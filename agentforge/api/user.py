from fastapi import APIRouter
from pydantic import BaseModel

from agentforge.utils import measure_time, comprehensive_error_handler
from agentforge.interfaces.model_profile import ModelProfile

router = APIRouter()

class StandardDictResponse(BaseModel):
  data: dict

@router.get('/{user_id}/model-profiles')
@comprehensive_error_handler
@measure_time
def get_user_profiles(user_id: str):
    model_profiles = ModelProfile()
    output = model_profiles.get_by_user(user_id)
    return output
