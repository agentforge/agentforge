#import logging
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel, validator
import traceback
import json
from typing import Optional
from tasks import master_scheduler, execute_event
from datetime import datetime
import random
from novu.api import EventApi
from novu.api.subscriber import SubscriberApi
from novu.dto.subscriber import SubscriberDto
import bleach
from agentforge.utils import logger
from supertokens_python.recipe.session.asyncio import get_session
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from supertokens_python.recipe.emailpassword.asyncio import get_user_by_id

# TO DO: Store in env var or config file
novu_url = "https://api.novu.co"
novu_api_key = "f9c8bc10975f2e9148a82aa87b8891db"


router = APIRouter()

# TO DO: store in environment variable
PUBLIC_APPLICATION_SERVER_KEY = "BPZjhYmoa74hrffBOS0flp3Sk_EcLuSFFww7iJ8HNFZe6JVx6tshoBQKT4GOZOxgBq81qqLAjEu9JKBwamCEELY"

# connecting within each endpoint avoids connection pooling pausing due to celery forks
# should raise max pool connections, currently at default of 10
def get_mongo_client():
    # This function returns a new MongoDB client instance.
    return MongoClient("mongodb://localhost:27017")

@router.post("/v1/create-schedule")
def create_schedule(request: Request, session: SessionContainer = Depends(verify_session())):
    session = await get_session(request)

    if session is None:
        raise Exception("User session not found.")

    user_id = session.get_user_id()

    try:
        data = await request.body()

        # Validate and sanitize event_name
        event_name = bleach.clean(data.get("event_name", ""), strip=True)
        if not event_name:
            raise HTTPException(status_code=400, detail="Invalid or missing event_name")

        # Additional validation for interval
        interval = data.get("interval", 0)
        if not isinstance(interval, int) or interval <= 0:
            raise HTTPException(status_code=400, detail="Invalid interval. Must be a positive integer.")

        # Create a new scheduled event in MongoDB with a timestamp
        current_time = datetime.utcnow()
        new_schedule = {
            "event_name": event_name,
            "interval": interval,
            "subscribed": 1,
            "last_execution_time": current_time
        }

        with get_mongo_client() as mongo_client:
            # Use the client to interact with the database
            db = mongo_client["agentforge"]
            schedule_collection = db["events"]

            result = schedule_collection.insert_one(new_schedule)
            new_schedule["_id"] = str(result.inserted_id) 

            # debugging
            #logger.info("New Schedule: %s", new_schedule)

            # Schedule the new event for execution using Celery
            master_scheduler.apply_async(countdown=data.interval * 60)  # Schedule in seconds
            return new_schedule

    except Exception as e:
        # Log other unexpected errors along with the traceback
        logger.error(f"Unexpected Error: {str(e)}")
        traceback.print_exc()  # Print the traceback
        raise  # Re-raise the exception to maintain FastAPI's default behavior

@router.post("/v1/delete-schedule/")
def delete_schedule(request: Request, session: SessionContainer = Depends(verify_session())):
    session = await get_session(request)

    if session is None:
        raise Exception("User session not found.")

    data = await request.body()

    # Validate and sanitize event_name
    event_name = bleach.clean(data.get("event_name", ""), strip=True)
    if not event_name:
        raise HTTPException(status_code=400, detail="Invalid or missing event_name")

    with get_mongo_client() as mongo_client:
            db = mongo_client["agentforge"]
            schedule_collection = db["events"]
            
            # Find and delete the scheduled event with the given event name
            result = schedule_collection.delete_one({"event_name": event_name})

            if result.deleted_count == 1:
                return {"message": f"Scheduled event with event name {event_name} deleted"}
            else:
                raise HTTPException(status_code=404, detail="Scheduled event not found")

@router.get("/v1/view-schedule")
def view_schedule(session: SessionContainer = Depends(verify_session())):
    session = await get_session(request)
    
    if session is None:
        raise Exception("User session not found.")

    try:
        with get_mongo_client() as mongo_client:
            db = mongo_client["agentforge"]
            schedule_collection = db["events"]

            # Return the list of scheduled events from MongoDB
            schedule_list = list(schedule_collection.find())
            
            # Convert ObjectId to string in the schedule_list
            for schedule in schedule_list:
                schedule["_id"] = str(schedule["_id"])

            json_content = json.dumps(jsonable_encoder(schedule_list), default=lambda x: str(x))
            return JSONResponse(content=json_content)
        
    except Exception as e:
        logger.error(f"Error in view_schedule: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")

# update an event
@router.post("/v1/update-schedule/")
def update_schedule(request: Request, session: SessionContainer = Depends(verify_session())):
    session = await get_session(request)
    
    if session is None:
        raise Exception("User session not found.")

    update_fields = {}

    data = await request.body()

    # Validate and sanitize event_name
    event_name = bleach.clean(data.get("event_name", ""), strip=True)
    if not event_name:
        raise HTTPException(status_code=400, detail="Invalid or missing event_name")

    # validate interval
    interval = data.get("interval", 0)
    if not isinstance(interval, int) or interval <= 0:
        raise HTTPException(status_code=400, detail="Invalid interval. Must be a positive integer.")

    # Check each field in the data object and add it to the update dictionary if it's not empty
    if event_name:
        update_fields["event_name"] = data.event_name

    if interval:
        update_fields["interval"] = data.interval

    with get_mongo_client() as mongo_client:
            db = mongo_client["agentforge"]
            schedule_collection = db["events"]

            # Check if there are any fields to update
            if update_fields:
                # Find and update the scheduled event with the given ID in MongoDB
                result = schedule_collection.update_one(
                    {"event_name": event_name},
                    {"$set": update_fields},
                )

                if result.modified_count == 1:
                    updated_schedule = schedule_collection.find_one({"event_name": event_name})

                    # only reschedule celery master if interval was changed
                    if "interval" in update_fields:
                        # Reschedule the event for execution using Celery
                        master_scheduler.apply_async(countdown=interval * 60)  # Schedule in seconds

                    return updated_schedule
                else:
                    raise HTTPException(status_code=404, detail="Scheduled event not found")
            else:
                # If no fields to update, return a response indicating that nothing was updated
                return {"message": "No fields to update"}

# subscribe to an event
@router.post("/v1/subscribe-schedule/")
def subscribe_schedule(request: Request, session: SessionContainer = Depends(verify_session())):
    session = await get_session(request)
    
    if session is None:
        raise Exception("User session not found.")

    data = await request.body()

    # Validate and sanitize event_name
    event_name = bleach.clean(data.get("event_name", ""), strip=True)

    if not event_name:
        raise HTTPException(status_code=400, detail="Invalid or missing event_name")


    with get_mongo_client() as mongo_client:
            db = mongo_client["agentforge"]
            schedule_collection = db["events"]

            # Find the scheduled event with the given event name
            existing_schedule = schedule_collection.find_one({"event_name": event_name})

            if existing_schedule:
                # Update the 'subscribe' field to 1 for subscribe
                schedule_collection.update_one(
                    {"event_name": event_name},
                    {"$set": {"subscribed": 1}}
                )

                return {"message": f"Scheduled event with event name {event_name} subscribed"}
            else:
                raise HTTPException(status_code=404, detail="Scheduled event not found")

# unsubscribe from event
@router.post("/v1/unsubscribe-schedule/")
def unsubscribe_schedule(request: Request, session: SessionContainer = Depends(verify_session())):
    session = await get_session(request)
    
    if session is None:
        raise Exception("User session not found.")

    data = await request.body()

    # Validate and sanitize event_name
    event_name = bleach.clean(data.get("event_name", ""), strip=True)

    if not event_name:
        raise HTTPException(status_code=400, detail="Invalid or missing event_name")

    with get_mongo_client() as mongo_client:
            db = mongo_client["agentforge"]
            schedule_collection = db["events"]

            # Find the scheduled event with the given event name
            existing_schedule = schedule_collection.find_one({"event_name": event_name})

            if existing_schedule:
                # Update the 'subscribe' field to 0 for unsubscribe
                schedule_collection.update_one(
                    {"event_name": event_name},
                    {"$set": {"subscribed": 0}}
                )

                return {"message": f"Scheduled event with event name {event_name} unsubscribed"}
            else:
                raise HTTPException(status_code=404, detail="Scheduled event not found")

class SubscriptionData(BaseModel):
    endpoint: str
    keys: dict

# hit when initially registering service worker,
# stores push notification object and create NOVU 
# subscriber
@router.post("/v1/subscribe-notifications")
def subscribe_notifications(request: Request, session: SessionContainer = Depends(verify_session())):
    session = await get_session(request)
    
    if session is None:
        raise Exception("User session not found.")

    try:
        # Ensure the required fields are present in the request body
        if not request.body.keys or not request.body.endpoint:
            raise HTTPException(status_code=400, detail="Incomplete push subscription data")

        # The domain of the endpoint is essentially the push service
        # The path of the endpoint is a client identifier information that 
        # helps the push service determine which client to push the notification to
        push_subscription = {
            "user_id": '1',             # TO DO: use user identifier...supertokens?
            "endpoint": request.body.endpoint,
            "keys": {
                "p256dh": request.body.keys.get("p256dh", ""),
                "auth": request.body.keys.get("auth", "")
            },
        }
        
        # debugging
        #logger.info("push_subscription: %s", push_subscription)

        with get_mongo_client() as mongo_client:
            db = mongo_client["agentforge"]
            users_collection = db["users"]

            # Check if the user is already subscribed               #TO DO: change user_id
            existing_subscription = users_collection.find_one({"push_subscription.user_id": 1, "push_subscription.endpoint": data.endpoint})


            if existing_subscription:
                raise HTTPException(status_code=400, detail="User is already subscribed")
            
            try:
                # Create NOVU subscriber instance
                novu_subscriber_id = random.random() # TO DO: replace with supertokens ID
                novu_subscriber = SubscriberDto(
                    subscriber_id=novu_subscriber_id,
                    email="abc@email.com",           #TO DO: replace with actual email? not sure if required
                    first_name="",                   # optional
                    last_name="",                    # optional
                    phone="",                        # optional
                    avatar=""                        # optional   
                )

                # Insert the new subscription data into the database
                result = users_collection.insert_one({
                    "novu_subscription": {
                        "id": novu_subscriber_id,
                        "email": novu_subscriber.email,
                        "first_name": novu_subscriber.first_name,
                        "last_name": novu_subscriber.last_name
                    },
                    "push_subscription": push_subscription,
                    "created_at": datetime.utcnow()
                })

            except Exception as e:
                error_message = f"Error creating NOVU subscriber and/or inserting subscription data: {str(e)}"
                logger.error(error_message)
                raise HTTPException(status_code=500, detail=error_message)

            if result.inserted_id:
                # Send the PushSubscription object back to the client
                return JSONResponse(content=push_subscription, status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@router.post("/v1/unsubscribe-notifications")
def unsubscribe_notifications(request: Request, session: SessionContainer = Depends(verify_session())):
    session = await get_session(request)
    
    if session is None:
        raise Exception("User session not found.")

    try:
        if not request.body.keys or not request.body.endpoint:
            raise HTTPException(status_code=400, detail="Incomplete push subscription data")

        with get_mongo_client() as mongo_client:
            db = mongo_client["agentforge"]
            users_collection = db["users"]

            # Check if the user is subscribed                 
            existing_subscription = users_collection.find_one({"push_subscription.endpoint": request.body.endpoint})
            if existing_subscription is None:
                raise HTTPException(status_code=404, detail="User is not subscribed")

            try:
                # Delete the subscription data from the database       
                result = users_collection.delete_one({"push_subscription.endpoint": request.body.endpoint})
            except Exception as e:
                error_message = f"Error deleting subscription data: {str(e)}"
                raise HTTPException(status_code=500, detail=error_message)

            if result.deleted_count > 0:
                # Successfully unsubscribed
                return {"message": "Unsubscribed successfully"}
            else:
                raise HTTPException(status_code=500, detail="Failed to unsubscribe")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")