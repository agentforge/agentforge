from fastapi import APIRouter, WebSocket
from agentforge.interfaces.vad.resource import process_chunk
from agentforge.utils import logger

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:          
          data = await websocket.receive_bytes()
        except Exception as e:
            logger.info(f"Error processing chunk: {str(e)}")
            break
        try:
           response = await process_chunk(data)
        except Exception as e:
            logger.info(f"Error processing chunk: {str(e)}")
            response = ""
        try:
            await websocket.send_text(response)
        except Exception as e:
            logger.info(f"Error sending response: {str(e)}")
            break
