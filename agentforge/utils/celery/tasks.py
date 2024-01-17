import asyncio
import json
from bson import ObjectId
from celery.utils.log import get_task_logger
from celery.signals import task_prerun, task_postrun
from datetime import datetime, timedelta
from pymongo import MongoClient
from celery_config import celery_app
from pywebpush import webpush, WebPushException

from novu.api import EventApi

# TO DO: Store in env var or config file
novu_url = "https://api.novu.co"
novu_api_key = "f9c8bc10975f2e9148a82aa87b8891db"

logger = get_task_logger(__name__)

# this approach avoids max pool pausing 
def get_mongo_client():
    # This function returns a new MongoDB client instance.
    return MongoClient("mongodb://localhost:27017")

# Function to query MongoDB for due events
def query_due_events_from_mongodb():
    try:
        current_time = datetime.utcnow()

        # Use the get_mongo_client function to get a MongoDB client instance
        with get_mongo_client() as mongo_client:
            # Use the client to interact with the database
            db = mongo_client["agentforge"]
            schedule_collection = db["events"]

            # Find events that are both due and subscribed
            due_and_subscribed_events = schedule_collection.find({
                "subscribed": 1,  # Only subscribed events
                "interval": {"$exists": True},  # Only events with interval defined
                "$expr": {
                    "$lte": [
                        "$last_execution_time",
                        {"$subtract": [current_time, {"$multiply": ["$interval", 60 * 1000]}]}
                    ]
                }
            })

            due_events_list = list(due_and_subscribed_events)
            print("Due Events List:", due_events_list)

            # Update last_execution_time for each due event
            for due_event in due_events_list:
                # Update the last_execution_time to the current time
                schedule_collection.update_one(
                    {"_id": due_event["_id"]},
                    {"$set": {"last_execution_time": current_time}}
                )

            return due_events_list

    except Exception as e:
        # Log the error or handle it as needed
        logger.error(f"Error in query_due_events_from_mongodb: {str(e)}")
        return []

# Function to retrieve event details from MongoDB
def get_event_from_mongodb(event_id):
    #from events import schedule_collection
    try:
        # Convert the provided event_id to ObjectId
        object_id = ObjectId(event_id)

        # Use the get_mongo_client function to get a MongoDB client instance
        with get_mongo_client() as mongo_client:
            # Use the client to interact with the database
            db = mongo_client["agentforge"]
            schedule_collection = db["events"]

            # Query MongoDB to find the event with the given _id
            event = schedule_collection.find_one({"_id": object_id})

            if event:
                return event
            else:
                raise Exception(f"Event with ID {event_id} not found in MongoDB")

    except Exception as e:
        # Log the error or handle it as needed
        logger.error(f"Error in get_event_from_mongodb: {str(e)}")
        raise  # Re-raise the exception to propagate it to the caller

# Function to send a notification
async def send_notification(event):
    try:
        # Replace this with logic to get the user_id from the event
        #user_id = event.get("user_id")
        user_id = "1"
        #logger.info(f"send_notification user_id: {str(user_id)}")

        # Use the get_mongo_client function to get a MongoDB client instance
        with get_mongo_client() as mongo_client:
            # Use the client to interact with the database
            db = mongo_client["agentforge"]
            users_collection = db["users"]

            # Retrieve the push subscription object from the users collection
            user = users_collection.find_one({"push_subscription.user_id": user_id})

            if user and "push_subscription" in user:
                push_subscription = user["push_subscription"]
                logger.info(f"push_subscription: {str(push_subscription)}")

                # Adapt push_subscription to the format expected by webpush
                formatted_subscription = {
                    'endpoint': push_subscription['endpoint'],
                    'keys': {
                        'p256dh': push_subscription['keys']['p256dh'],
                        'auth': push_subscription['keys']['auth']
                    }
                }
                
                # I think I got my IP blocked for too many requests while testing :( notifications thru NOVU were working tho
                
                # NOVU event notification
                # novu = EventApi(novu_url, novu_api_key).trigger(
                #     name="schedule",  # The trigger ID of the workflow. It can be found on the workflow page.
                #     recipients="123456789", # subscriber (user) ID
                #     payload={"tenant.data": str(event)}, # notification payload
                # )

                # Retrieve the event_name from the event
                event_name = event.get("event_name")
                try:
                    # Send the push message using pywebpush   
                    webpush(
                        subscription_info=formatted_subscription,
                        data=f"{event_name}",
                        vapid_private_key='v19NCEd4-9zM6XaexzGBHResKkgmDWbniZgo6vY7Lvw', # TO DO: store key in env var or .pem
                        vapid_claims={
                            "sub": "mailto:your@email.com",
                        }
                    )
                    #logger.info(f"sending webpush: {str(webpush)}")
                except WebPushException as ex:
                    logger.error(f"pywebpush error in send_notification: {repr(ex)}")
            else:
                logger.error(f"Push subscription not found for user with ID {user_id}")

    except Exception as e:
        # Log the error or handle it as needed
        logger.error(f"send_notification: {str(e)}")
        raise  # Re-raise the exception to propagate it to the caller  

# master scheduler celery task runs every minute and checks db for due events
@celery_app.task(name="master_scheduler")
def master_scheduler():
    try:
        logger.info("Running master scheduler task")

        # Query MongoDB for due events
        due_events = query_due_events_from_mongodb()

        # Trigger execute_event task for each due event
        for event in due_events:
            execute_event.apply_async(args=[str(event["_id"])], countdown=1)  # Convert ObjectId to string

        return len(due_events)  # Return the number of tasks scheduled

    except Exception as e:
        logger.error(f"Error in master_scheduler: {str(e)}")
        # Handle the exception as needed
    
# execute event celery task is called by master scheduler for due events        
@celery_app.task(name="execute_event")
def execute_event(event_id):
    try:
        logger.info(f"Executing event with ID {event_id}")

        # Perform event-specific logic
        event = get_event_from_mongodb(event_id)
        print(f"event: {str(event)}")

        # Optionally send a notification
        asyncio.run(send_notification(event))

    except Exception as e:
        logger.error(f"Error in execute_event for event {event_id}: {str(e)}")
        # Handle the exception as needed