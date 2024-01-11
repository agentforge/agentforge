from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel
import traceback
import json
from typing import Optional
from tasks import master_scheduler, execute_event
from datetime import datetime

# Public Application Server Key for Push Notifications:
# BPZjhYmoa74hrffBOS0flp3Sk_EcLuSFFww7iJ8HNFZe6JVx6tshoBQKT4GOZOxgBq81qqLAjEu9JKBwamCEELY

# Private Application Server Key for Push Notifications:
# v19NCEd4-9zM6XaexzGBHResKkgmDWbniZgo6vY7Lvw

router = APIRouter()

class ScheduleData(BaseModel):
    event_name: str
    interval: Optional[int] = None 
    validation_logic: Optional [str] = None 
    notification_method: Optional[str] = None

# TO DO: store in environment variable
PUBLIC_APPLICATION_SERVER_KEY = "BPZjhYmoa74hrffBOS0flp3Sk_EcLuSFFww7iJ8HNFZe6JVx6tshoBQKT4GOZOxgBq81qqLAjEu9JKBwamCEELY"

# Connect to MongoDB
mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client["agentforge"]
schedule_collection = db["events"]
users_collection = db["users"]

# Custom JSON encoder to handle ObjectId serialization
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

# Dependency to use the custom JSON encoder
def get_jsonable_encoder():
    return CustomJSONEncoder()

@router.post("/v1/create-schedule")
def create_schedule(data: ScheduleData):
    try:
        print("Received Payload:", data)
        if not event_name:
            raise HTTPException(status_code=400, detail="Invalid input data")

        # Create a new scheduled event in MongoDB with a timestamp
        current_time = datetime.utcnow()
        new_schedule = {
            "event_name": data.event_name,
            "interval": data.interval,
            "subscribed": 1,
            "timestamp": current_time
        }

        result = schedule_collection.insert_one(new_schedule)
        new_schedule["_id"] = str(result.inserted_id) 

        # Log information for debugging
        print("New Schedule:", new_schedule)

        # Schedule the new event for execution using Celery
        master_scheduler.apply_async(countdown=data.interval * 60)  # Schedule in seconds
        return new_schedule

    except Exception as e:
        # Log other unexpected errors along with the traceback
        print(f"Unexpected Error: {str(e)}")
        traceback.print_exc()  # Print the traceback
        raise  # Re-raise the exception to maintain FastAPI's default behavior

@router.post("/v1/delete-schedule/")
def delete_schedule(data: ScheduleData):
    # Retrieve event_name from the request body
    event_name = data.event_name

    if not event_name:
        raise HTTPException(status_code=400, detail="Event name is required in the request body")

    # Find and delete the scheduled event with the given event name
    result = schedule_collection.delete_one({"event_name": event_name})

    if result.deleted_count == 1:
        return {"message": f"Scheduled event with event name {event_name} deleted"}
    else:
        raise HTTPException(status_code=404, detail="Scheduled event not found")

@router.get("/v1/view-schedule")
def view_schedule():
    try:
        # Return the list of scheduled events from MongoDB
        schedule_list = list(schedule_collection.find())
        
        # Convert ObjectId to string in the schedule_list
        for schedule in schedule_list:
            schedule["_id"] = str(schedule["_id"])

        json_content = json.dumps(jsonable_encoder(schedule_list), default=lambda x: str(x))
        return JSONResponse(content=json_content)
    except Exception as e:
        print(f"Error in view_schedule: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/v1/update-schedule/")
def update_schedule(data: ScheduleData):
    # Create a dictionary to store the fields that need to be updated
    update_fields = {}

    # Check each field in the data object and add it to the update dictionary if it's not empty
    if data.event_name:
        update_fields["event_name"] = data.event_name

    if data.interval:
        update_fields["interval"] = data.interval

    if data.validation_logic:
        update_fields["validation_logic"] = data.validation_logic

    # Check if there are any fields to update
    if update_fields:
        # Find and update the scheduled event with the given ID in MongoDB
        result = schedule_collection.update_one(
            {"event_name": data.event_name},
            {"$set": update_fields},
        )

        if result.modified_count == 1:
            updated_schedule = schedule_collection.find_one({"event_name": data.event_name})

            # Reschedule the event for execution using Celery
            master_scheduler.apply_async(countdown=data.interval * 60)  # Schedule in seconds

            return updated_schedule
        else:
            raise HTTPException(status_code=404, detail="Scheduled event not found")
    else:
        # If no fields to update, return a response indicating that nothing was updated
        return {"message": "No fields to update"}
    
@router.post("/v1/subscribe-schedule/")
def subscribe_schedule(data: ScheduleData):
    event_name = data.event_name

    if not event_name:
        raise HTTPException(status_code=400, detail="Event name is required in the request body")

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

@router.post("/v1/unsubscribe-schedule/")
def unsubscribe_schedule(data: ScheduleData):
    event_name = data.event_name

    if not event_name:
        raise HTTPException(status_code=400, detail="Event name is required in the request body")

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

@router.post("/v1/subscribe-notifications")
def subscribe_notifications(data: SubscriptionData):
    try:
        # Ensure the required fields are present in the request body
        if not data.keys or not data.endpoint:
            raise HTTPException(status_code=400, detail="Incomplete subscription data")

        # Include the VAPID public key in the response
        #TO DO: THIS MAY BE IN THE WRONG FORMAT
        push_subscription = {
            "user_id": '1',             # TO DO: Get user identifier...supertokens?
            "endpoint": data.endpoint,
            "keys": {
                "p256dh": data.keys.get("p256dh", ""),
                "auth": data.keys.get("auth", "")
            },
            #"publicKey": PUBLIC_APPLICATION_SERVER_KEY  # Include the VAPID public key
        }
        
        print("push_subscription: ", push_subscription)

        # Check if the user is already subscribed
        # The domain of the endpoint is essentially the push service. 
        # The path of the endpoint is client identifier information that helps the push service determine 
        # exactly which client to push the notification/message to
        existing_subscription = users_collection.find_one({"endpoint": data.endpoint})

        if existing_subscription:
            raise HTTPException(status_code=400, detail="User is already subscribed")

         # Insert the new subscription data into the database
        result = users_collection.insert_one({
            "push_subscription": push_subscription
        })

        print("result: ", result)

        if result.inserted_id:
            # Send the PushSubscription object back to the client
            return JSONResponse(content=push_subscription, status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
