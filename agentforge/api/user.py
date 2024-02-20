from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from agentforge.interfaces.mongodb import MongoDBKVStore as DB
from agentforge.config import DbConfig
from agentforge.utils import measure_time, comprehensive_error_handler
from agentforge.interfaces.model_profile import ModelProfile
from supertokens_python.recipe import emailpassword
from supertokens_python.recipe.emailpassword.interfaces import ResetPasswordUsingTokenOkResult, ResetPasswordUsingTokenInvalidTokenError
router = APIRouter()

class StandardDictResponse(BaseModel):
  data: dict

@router.get('/{user_id}/model-profiles', operation_id="listModelProfilesByUser")
@comprehensive_error_handler
@measure_time
def get_user_profiles(user_id: str):
    model_profiles = ModelProfile()
    output = model_profiles.get_by_user(user_id)
    return output

db_config = DbConfig.from_env()

@router.post("/generate-reset-token")
async def generate_reset_token(request: Request):
    body = await request.json()
    email = body.get('email')

    if not email:
        raise HTTPException(status_code=400, detail="Missing email")

    # Use SuperTokens to find user ID by email
    user = await emailpassword.EmailPasswordRecipe.get_instance().recipe_implementation.get_user_by_email(email, "public", {})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.user_id

    # Create reset password token using SuperTokens
    try:
        token = await emailpassword.EmailPasswordRecipe.get_instance().recipe_implementation.create_reset_password_token(user_id, "public", {})
        return {"token": token.token}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error generating reset token")

@router.post("/reset-password")
async def reset_password(request: Request):
    body = await request.json()
    password = body.get('password')
    token = body.get('token')

    if not password or not token:
        print("missing parameters")
        raise HTTPException(status_code=400, detail="Missing parameters")

    # Perform the password reset using SuperTokens
    result = await emailpassword.EmailPasswordRecipe.get_instance().recipe_implementation.reset_password_using_token(
        token, password, "public", {}
    )
    print(result)

    # Check the type of result and respond accordingly
    if isinstance(result, ResetPasswordUsingTokenOkResult):
        # If the password reset is successful
        return {"status": "success"}

    elif isinstance(result, ResetPasswordUsingTokenInvalidTokenError):
        # If the token is invalid
        raise HTTPException(status_code=400, detail="Invalid or Expired Token")

    else:
        # Handle unexpected results
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

