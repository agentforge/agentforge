from fastapi import HTTPException
from supertokens_python.recipe.emailpassword.interfaces import RecipeInterface, SignInOkResult, SignUpOkResult
from supertokens_python.recipe.session.interfaces import RecipeInterface
from typing import Dict, Any, Optional
from agentforge.interfaces.mongodb import MongoDBKVStore as DB
from agentforge.config import DbConfig
from datetime import datetime

db_config = DbConfig.from_env()
db = DB(db_config)  # Initialize your DB class here

def override_functions(original_implementation: RecipeInterface):
    original_implementation_create_new_session = original_implementation.create_new_session

    async def create_new_session(user_id: str,
                                 access_token_payload: Optional[Dict[str, Any]],
                                 session_data_in_database: Optional[Dict[str, Any]],
                                 disable_anti_csrf: Optional[bool],
                                 tenant_id: str,
                                 user_context: Dict[str, Any]):
        if access_token_payload is None:
            access_token_payload = {}

        # This goes in the access token, and is available to read on the frontend.
        print(user_id)
        user = db.get_many("users", {"supertokens_id" :user_id })
        if user:
            print(user[0]['email'])
            access_token_payload["email"] = user[0]['email']
            # access_token_payload["last_login"] = user[0]['last_login']

        # access_token_payload["someKey"] = 'someValue'
        # TODO: Get user email and add to session information

        return await original_implementation_create_new_session(user_id, access_token_payload, session_data_in_database, disable_anti_csrf, tenant_id, user_context)

    original_implementation.create_new_session = create_new_session
    return original_implementation


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
        print(existing_user)
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
