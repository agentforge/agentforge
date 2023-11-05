from fastapi import APIRouter, WebSocket
from agentforge.interfaces.vad.resource import VadWhisper
from agentforge.utils import logger

router = APIRouter()
vw = VadWhisper()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:          
          data = await websocket.receive_bytes()
        except Exception as e:
            logger.info(f"Error processing chunk: {str(e)}")
            # raise Exception(e)
        try:
           response = await vw.process_chunk(data)
        except Exception as e:
            logger.info(f"Error processing chunk: {str(e)}")
            # raise Exception(e)
        try:
            await websocket.send_text(response)
        except Exception as e:
            logger.info(f"Error sending response: {str(e)}")
            # raise Exception(e)
