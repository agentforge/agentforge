# from typing import Any, Optional, Dict
# from fastapi.security.api_key import APIKeyHeader
# from fastapi import HTTPException, Security
# from datetime import datetime, timedelta
# from fastapi import APIRouter
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt, ExpiredSignatureError
# from passlib.context import CryptContext
# from typing import Optional
# from pydantic import BaseModel
# from agentforge.interfaces import interface_interactor
# import traceback

# # Security for API
# # TODO: Need to make this multi-user one day!
# API_KEY = "test-api-key-for-agent-forge-banana-mark-one"
# API_KEY_NAME = "X-API-KEY"

# api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# def get_api_key(api_key_header: str = Security(api_key_header)):
#     if api_key_header != API_KEY:
#         raise HTTPException(status_code=403, detail="Unauthorized")
#     return api_key_header

# ### Security for users: JWT Tokens
# # to get a string like this run:
# # openssl rand -hex 32
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }

# class UserIdForm(BaseModel):
#     user_id: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# router = APIRouter()
# db = interface_interactor.get_interface("db")

# def verify_token_exists(data: Dict[str, Any]) -> bool:
#     if "apiToken" not in data:
#         raise Exception({"error": "apiToken is not found in API input"})
#     token_record = db.get("tokens", data["apiToken"])
#     if token_record is not None:
#         return token_record
#     return None

# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     user_id = data.get("sub")

#     # Try to retrieve an existing token from the database
#     existing_token_record = db.get("tokens", user_id) if user_id else None

#     if existing_token_record:
#         existing_token = existing_token_record.get("token")
        
#         # Verify the existing token
#         try:
#             payload = jwt.decode(existing_token, SECRET_KEY, algorithms=[ALGORITHM])
#             # If decoding is successful and doesn't raise an exception, the token is valid and not expired
#             return existing_token
#         except ExpiredSignatureError:
#             # The token is expired, we'll generate a new one below
#             pass
#         except JWTError:
#             # The token is invalid, we'll generate a new one below
#             pass

#     # If we're here, we need to generate a new token
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     new_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#     # Save the new token in the database #TODO: Ideally we don't save these in DB and use shared SECRET_KEY/ALGORITHM to determine validity
#     if user_id:
#         db.set("tokens", new_token, {"user_id": user_id, "expiry": expire})

#     return new_token

# @router.post("/token", response_model=Token)
# def login_for_access_token(user: UserIdForm):
#     try:
#       # check if token exists for this userId, if so return existing token
#       # TODO
#       # if token does not exist create a new token and save it in the DB
#       access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#       access_token = create_access_token(
#           data={"sub": user.user_id}, expires_delta=access_token_expires
#       )
#       return {"access_token": access_token, "token_type": "bearer"}
#     except Exception as e:
#       print(e)
#       print(traceback.format_exc())