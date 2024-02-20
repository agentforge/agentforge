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

from agentforge.adapters import DB
from mongodb import MongoDBKVStore

# TO DO: Store in env var or config file
#novu_url = "https://api.novu.co"
#novu_api_key = "f9c8bc10975f2e9148a82aa87b8891db"

logger = get_task_logger(__name__)

mongo_client = MongoDBKVStore(DB)

# Function to query MongoDB for due events
def get_due_events(session: SessionContainer = Depends(verify_session())):
    try:
        supertokens_id = session.get_user_id()

        # Query MongoDB for due events using MongoDBKVStore
        current_time = datetime.utcnow()
        user = mongo_client.find_one("users", {"supertokens_id": supertokens_id})

        if user and "events" in user:
            due_events = []
            for event in user["events"]:
                if (
                    event.get("subscribed") == 1
                    and event.get("interval", 0) > 0
                    and event.get("last_execution_time", datetime.min)
                    <= current_time - timedelta(minutes=event["interval"]) # minutes for testing
                ):
                    # Update last_execution_time for each due event
                    mongo_client.update_one(
                        "users",
                        {
                            "supertokens_id": supertokens_id,
                            "events._id": event["_id"],
                        },
                        {"$set": {"events.$.last_execution_time": current_time}},
                    )
                    due_events.append(event)

            return due_events

        return []

    except Exception as e:
        logger.error(f"Error in get_due_events: {str(e)}")
        return []

# Function to retrieve event details from MongoDB
def get_event_from_mongodb(event_id):
    #from events import schedule_collection
    try:
        object_id = ObjectId(event_id)
        supertokens_id = session.get_user_id()

        # Query MongoDB for due events using MongoDBKVStore
        user = mongo_client.find_one("users", {"supertokens_id": supertokens_id})

        if user and "events" in user:
            # Search for the event within the "events" field of the user document
            events = user["events"]
            event = next((e for e in events if e["_id"] == object_id), None)

            if event:
                return event
            else:
                raise HTTPException(status_code=404, detail=f"Event with ID {event_id} not found for the user")

        else:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found or has no events")

    except HTTPException:
        # Re-raise HTTPException to propagate it to the caller
        raise

    except Exception as e:
        # Log the error or handle it as needed
        logger.error(f"Error in get_event_from_mongodb: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Function to send a notification
async def send_notification(session, event):
    try:
        supertokens_id = session.get_user_id()

        # Query MongoDBKVStore to find the user with the given supertokens_id
        user = mongo_db_store.find_one("users", {"supertokens_id": supertokens_id})

        if user and "push_subscription" in user:
            push_subscription = user["push_subscription"]
            #logger.info(f"push_subscription: {str(push_subscription)}")

            # Adapt push_subscription to the format expected by webpush
            formatted_subscription = {
                'endpoint': push_subscription['endpoint'],
                'keys': {
                    'p256dh': push_subscription['keys']['p256dh'],
                    'auth': push_subscription['keys']['auth']
                }
            }
            
            # I think I got my IP blocked for too many requests while testing :(
            # Notifications through NOVU were working though
            
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
            logger.error(f"Push subscription not found for user with supertokens_id {supertokens_id}")

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
        due_events = get_due_events()

        # Trigger execute_event task for each due event
        for event in due_events:
            execute_event.apply_async(args=[str(event["_id"])], countdown=1)  # Convert ObjectId to string

        return len(due_events)  # Return the number of tasks scheduled

    except Exception as e:
        logger.error(f"Error in celery master_scheduler: {str(e)}")
    
# execute event celery task is called by master scheduler for due events        
@celery_app.task(name="execute_event")
def execute_event(event_id):
    try:
        logger.info(f"Executing event with ID {event_id}")

        # get event based on event_id
        event = get_event_from_mongodb(event_id)

        # send a notification
        asyncio.run(send_notification(event))

    except Exception as e:
        logger.error(f"Error in celery execute_event for event {event_id}: {str(e)}")
        # Handle the exception as needed