from fastapi import APIRouter, Request
from pydantic import BaseModel

from agentforge.utils import measure_time, comprehensive_error_handler
from agentforge.interfaces.model_profile import ModelProfile

router = APIRouter()

class ModelProfileResponse(BaseModel):
  data: dict

@router.post('')
async def create_profile(request: Request) -> ModelProfileResponse:
    model_profiles = ModelProfile()
    data = request.get_json()  # retrieve data from the POST request body
    output = model_profiles.create(data)
    return ModelProfileResponse(data=output)

@router.post('/copy/{id}')
async def copy_profile(id: str) -> ModelProfileResponse:
    model_profiles = ModelProfile()
    return ModelProfileResponse(data={"success": model_profiles.copy(id)})

@router.put('/{id}')
async def put(id: str, request: dict) -> ModelProfileResponse:
    model_profiles = ModelProfile()
    data = request.get_json()  # retrieve data from the PUT request body
    return ModelProfileResponse(data=model_profiles.set(id, data))

@router.get('/{id}')
async def get_model_profile(id: str) -> ModelProfileResponse:
    model_profiles = ModelProfile()
    print(model_profiles)
    return ModelProfileResponse(data=model_profiles.get(id))

@router.delete('/{id}')
async def delete_model_profile(id: str) -> ModelProfileResponse:
    model_profiles = ModelProfile()
    return ModelProfileResponse(data=model_profiles.delete(id))

