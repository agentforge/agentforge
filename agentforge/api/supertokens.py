from fastapi import HTTPException
from supertokens_python.recipe.emailpassword.interfaces import RecipeInterface, SignInOkResult, SignUpOkResult
from typing import Dict, Any
from agentforge.interfaces.mongodb import MongoDBKVStore as DB
from agentforge.config import DbConfig
from datetime import datetime

db_config = DbConfig.from_env()
db = DB(db_config)  # Initialize your DB class here

def override_emailpassword_functions(original_implementation: RecipeInterface) -> RecipeInterface:
    original_emailpassword_sign_up = original_implementation.sign_up
    original_emailpassword_sign_in = original_implementation.sign_in

    async def emailpassword_sign_up(
        email: str,
        password: str,
        tenant_id: str,
        user_context: Dict[str, Any]
    ):
        # Pre sign-up logic: Check if user already exists in DB
        existing_user = db.get("users", email)
        if existing_user:
            raise HTTPException(status_code=500, detail="User already exists.")

        # Proceed with original sign-up logic
        result = await original_emailpassword_sign_up(email, password, tenant_id, user_context)

        if isinstance(result, SignUpOkResult):
            # Post sign-up logic: Save user to DB
            user_data = {
                "email": email,
                "supertokens_id": result.user.user_id,
            }
            db.create("users", data=user_data)

        return result

    async def emailpassword_sign_in(
        email: str,
        password: str,
        tenant_id: str,
        user_context: Dict[str, Any]
    ):
        # Pre sign-in logic: Fetch user from DB
        existing_user = db.get_many("users", {'email': email})
        if not existing_user:
          raise HTTPException(status_code=401, detail="User not found.")

        # Proceed with original sign-in logic
        result = await original_emailpassword_sign_in(email, password, tenant_id, user_context)

        if isinstance(result, SignInOkResult):
            # Example: Update some field in DB
            user_data = {
                "email": email,
                "supertokens_id": result.user.user_id,
                "last_login": datetime.utcnow(),
            }
            db.set("users", existing_user[0]['id'], user_data)

        return result

    original_implementation.sign_up = emailpassword_sign_up
    original_implementation.sign_in = emailpassword_sign_in

    return original_implementation
