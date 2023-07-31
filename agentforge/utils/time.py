from datetime import datetime
from bson import ObjectId
import pytz

def get_mongo_timestamp(timezone=None):
    # Get current timezone if none is provided
    if timezone is None:
        current_datetime = datetime.now()
    else:
        current_datetime = datetime.now(pytz.timezone(timezone))
    
    # MongoDB timestamp - BSON Date type
    mongo_timestamp = current_datetime.timestamp() * 1000

    return mongo_timestamp

def timestamp_to_string(mongo_timestamp, timezone=None):
    # Convert MongoDB timestamp to seconds from milliseconds
    timestamp_in_seconds = mongo_timestamp / 1000

    # Convert timestamp to datetime object
    if timezone is None:
        datetime_obj = datetime.fromtimestamp(timestamp_in_seconds)
    else:
        datetime_obj = datetime.fromtimestamp(timestamp_in_seconds, pytz.timezone(timezone))

    # Convert datetime object to string in natural language
    datetime_str = datetime_obj.strftime("%A, %d %B %Y, %I:%M:%S %p %Z%z")

    return datetime_str