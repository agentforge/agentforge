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

from agentforge.adapters import DB
from mongodb import MongoDBKVStore


# TO DO: Store in env var or config file
novu_url = "https://api.novu.co"
novu_api_key = "f9c8bc10975f2e9148a82aa87b8891db"

router = APIRouter()

# TO DO: store in environment variable
PUBLIC_APPLICATION_SERVER_KEY = "BPZjhYmoa74hrffBOS0flp3Sk_EcLuSFFww7iJ8HNFZe6JVx6tshoBQKT4GOZOxgBq81qqLAjEu9JKBwamCEELY"

# may need to instantiate mongo_client in each endpoint to avoid connection pooling pausing due to celery forks
# should raise max pool connections, currently at default of 10
mongo_client = MongoDBKVStore(DB)

@router.post("/create-schedule")
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

        # Find the user based on user_id
        user_document = mongo_client.get("users", key=user_id)

        if user_document:
            # Check if "events" field exists in the user document, if not, create it
            if "events" not in user_document:
                user_document["events"] = {}

            # Check if the event_name already exists for the user
            if event_name in user_document["events"]:
                raise HTTPException(status_code=400, detail="Event with the same name already exists for the user.")

            # Insert the new schedule into the user's "events" field
            user_document["events"][event_name] = new_schedule

            # Use the MongoDBKVStore instance to update the user document
            mongo_client.set("users", key=user_id, data=user_document)

            # Schedule the new event for execution using Celery
            master_scheduler.apply_async(countdown=data.interval * 60)  # Schedule in seconds

            return new_schedule
        else:
            raise HTTPException(status_code=404, detail="User not found.")

    except HTTPException as http_exception:
        raise http_exception

    except Exception as e:
        # Log other unexpected errors along with the traceback
        logger.error(f"Unexpected Error: {str(e)}")
        traceback.print_exc()  # Print the traceback
        raise  # Re-raise the exception to maintain FastAPI's default behavior

@router.post("/delete-schedule")
def delete_schedule(request: Request, session: SessionContainer = Depends(verify_session())):
    session = await get_session(request)

    if session is None:
        raise Exception("User session not found.")

    data = await request.body()

    # Validate and sanitize event_name
    event_name = bleach.clean(data.get("event_name", ""), strip=True)
    if not event_name:
        raise HTTPException(status_code=400, detail="Invalid or missing event_name")

    user_id = session.get_user_id()

    # Find the user based on user_id
    user_document = mongo_client.get("users", key=user_id)

    if user_document and "events" in user_document:
        # Check if the event_name exists for the user
        if event_name in user_document["events"]:
            # Use the MongoDBKVStore instance to delete the event from the user's "events" field
            mongo_client.delete("users", key=user_id)
            return {"message": f"Scheduled event with event name {event_name} deleted"}
        else:
            raise HTTPException(status_code=404, detail="Scheduled event not found")
    else:
        raise HTTPException(status_code=404, detail="User not found or user has no scheduled events.")

@router.get("/view-schedule")
def view_schedule(session: SessionContainer = Depends(verify_session())):
    session = await get_session(request)
    
    if session is None:
        raise Exception("User session not found.")

    user_id = session.get_user_id()

    # Retrieve the user document from MongoDB using MongoDBKVStore
    user_document = mongo_client.get("users", key=user_id)

    if user_document and "events" in user_document:
        json_content = json.dumps(jsonable_encoder(user_document["events"]), default=lambda x: str(x))
        return JSONResponse(content=json_content)
    else:
        raise HTTPException(status_code=404, detail="User not found or user has no scheduled events.")

# update an event
@router.post("/update-schedule/")
def update_schedule(request: Request, session: SessionContainer = Depends(verify_session())):
    session = await get_session(request)
    
    if session is None:
        raise Exception("User session not found.")
    
    user_id = session.get_user_id()
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

     try:
        # Update the scheduled event in the user's "events" field using MongoDBKVStore
        result = mongo_client.set("users", key=user_id, data={"events": {event_name: update_fields}})

        if result:
            # only reschedule celery master if interval was changed
            if "interval" in update_fields:
                # Reschedule the event for execution using Celery
                master_scheduler.apply_async(countdown=interval * 60)  # Schedule in seconds

            return {"message": "Scheduled event updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found or scheduled event not found")
    except Exception as e:
        logger.error(f"Error updating scheduled event: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")

# subscribe to an event
@router.post("/subscribe-schedule/")
def subscribe_schedule(request: Request, session: SessionContainer = Depends(verify_session())):
    session = await get_session(request)
    
    if session is None:
        raise Exception("User session not found.")

    user_id = session.get_user_id()

    data = await request.body()

    # Validate and sanitize event_name
    event_name = bleach.clean(data.get("event_name", ""), strip=True)
    if not event_name:
        raise HTTPException(status_code=400, detail="Invalid or missing event_name")

    try:
        # Update the 'subscribed' field for the scheduled event in the user's "events" field using MongoDBKVStore
        result = mongo_client.set("users", key=user_id, data={"events": {event_name: {"subscribed": 1}}})

        if result:
            return {"message": f"Scheduled event with event name {event_name} subscribed"}
        else:
            raise HTTPException(status_code=404, detail="User not found or scheduled event not found")
    except Exception as e:
        logger.error(f"Error subscribing to scheduled event: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")

# unsubscribe from event
@router.post("/unsubscribe-schedule/")
def unsubscribe_schedule(request: Request, session: SessionContainer = Depends(verify_session())):
    session = await get_session(request)
    
    if session is None:
        raise Exception("User session not found.")

    user_id = session.get_user_id()

    data = await request.body()

    # Validate and sanitize event_name
    event_name = bleach.clean(data.get("event_name", ""), strip=True)
    if not event_name:
        raise HTTPException(status_code=400, detail="Invalid or missing event_name")

    try:
        # Update the 'subscribed' field to 0 for the scheduled event in the user's "events" field using MongoDBKVStore
        result = mongo_client.set("users", key=user_id, data={"events": {event_name: {"subscribed": 0}}})

        if result:
            return {"message": f"Scheduled event with event name {event_name} unsubscribed"}
        else:
            raise HTTPException(status_code=404, detail="User not found or scheduled event not found")
    except Exception as e:
        logger.error(f"Error unsubscribing from scheduled event: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")


class SubscriptionData(BaseModel):
    endpoint: str
    keys: dict

# hit when initially registering service worker,
# stores push notification object and create NOVU 
# subscriber
@router.post("/subscribe-notifications")
def subscribe_notifications(request: Request, session: SessionContainer = Depends(verify_session())):
    session = await get_session(request)
    
    if session is None:
        raise Exception("User session not found.")

    user_id = session.get_user_id()

    try:
        data = await request.json()

        # Ensure the required fields are present in the request body
        if not data.get("keys") or not data.get("endpoint"):
            raise HTTPException(status_code=400, detail="Incomplete push subscription data")

        # The domain of the endpoint is essentially the push service
        # The path of the endpoint is a client identifier information that 
        # helps the push service determine which client to push the notification to
        push_subscription = {
            "user_id": user_id,
            "endpoint": data.get("endpoint"),
            "keys": {
                "p256dh": data.get("keys").get("p256dh", ""),
                "auth": data.get("keys").get("auth", "")
            },
        }

        # Check if the user is already subscribed
        existing_subscription = mongo_client.get("users", key=user_id)

        if existing_subscription and existing_subscription.get("push_subscription", {}).get("endpoint") == data.get("endpoint"):
            raise HTTPException(status_code=400, detail="User is already subscribed")

        try:
            # Create NOVU subscriber instance
            novu_subscriber_id = random.random()  # TO DO: replace with supertokens ID
            novu_subscriber = SubscriberDto(
                subscriber_id=novu_subscriber_id,
                email="abc@email.com",           # TO DO: replace with actual email? not sure if required
                first_name="",                   # optional
                last_name="",                    # optional
                phone="",                        # optional
                avatar=""                        # optional   
            )

            # Update the user's information with the new subscription data using MongoDBKVStore
            result = mongo_client.set(
                "users",
                key=user_id,
                data={
                    "novu_subscription": {
                        "id": novu_subscriber_id,
                        "email": novu_subscriber.email,
                        "first_name": novu_subscriber.first_name,
                        "last_name": novu_subscriber.last_name
                    },
                    "push_subscription": push_subscription,
                    "created_at": datetime.utcnow()
                }
            )

        except Exception as e:
            error_message = f"Error creating NOVU subscriber and/or inserting subscription data: {str(e)}"
            logger.error(error_message)
            raise HTTPException(status_code=500, detail=error_message)

        if result:
            # Send the PushSubscription object back to the client
            return JSONResponse(content=push_subscription, status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@router.post("/unsubscribe-notifications")
def unsubscribe_notifications(request: Request, session: SessionContainer = Depends(verify_session())):
    session = await get_session(request)
    
    if session is None:
        raise Exception("User session not found.")

    user_id = session.get_user_id()

    try:
        data = await request.json()

        # Ensure the required fields are present in the request body
        if not data.get("keys") or not data.get("endpoint"):
            raise HTTPException(status_code=400, detail="Incomplete push subscription data")

        # Check if the user is subscribed
        existing_subscription = mongo_client.get("users", key=user_id)

        if existing_subscription and existing_subscription.get("push_subscription", {}).get("endpoint") != data.get("endpoint"):
            raise HTTPException(status_code=404, detail="User is not subscribed")

        try:
            # Delete the subscription data from the database using MongoDBKVStore
            result = mongo_client.delete("users", key=user_id)
        except Exception as e:
            error_message = f"Error deleting subscription data: {str(e)}"
            raise HTTPException(status_code=500, detail=error_message)

        if result:
            # Successfully unsubscribed
            return {"message": "Unsubscribed successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to unsubscribe")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")