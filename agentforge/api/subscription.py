from fastapi import APIRouter, HTTPException
from agentforge.interfaces.mongodb import MongoDBKVStore as DB
from agentforge.config import DbConfig
import time
from pydantic import BaseModel
from supertokens_python.recipe.session.asyncio import get_session
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session import SessionContainer
from fastapi import Depends, Request

class UserEmail(BaseModel):
    email: str

router = APIRouter()

db_config = DbConfig.from_env()
db = DB(db_config)  # Initialize your DB class here

@router.post("/check-subscription")
async def check_subscription(request: Request, session: SessionContainer = Depends(verify_session)):
    print(session)
    session = await get_session(request)

    if session is None:
        raise HTTPException(status_code=401, detail="User session not found.")

    user_id = session.get_user_id()
    cursor = db.get_many("users", {'supertokens_id': user_id})  # This returns a Cursor
    user_data_list = list(cursor)  # Convert Cursor to list of dictionaries

    if not user_data_list:
        return {"message": "user not found/has not paid", "status": 200}

    user_data = user_data_list[0]  # Get the first item (should only be one)
    user_email = user_data.get("email")

    if user_data:
        check_paid = db.get_many("users", {"email": user_email, "subscription.status": "active"})

        if check_paid and 'cancel_at' in user_data.get("subscription", {}):
            cancel_at = check_paid[0].get("subscription", {}).get("cancel_at")
            if cancel_at:
                current_time = int(time.time())
                if current_time < cancel_at:
                    return {"message": "subscription active", "status": 200}
                else:
                    return {"message": "subscription inactive", "status": 200}
            else:
                return {"message": "subscription active", "status": 200}
        else:
            return {"message": "subscription inactive", "status": 200}
    else:
        return {"message": "user not found/has not paid", "status": 200}