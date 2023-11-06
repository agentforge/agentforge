from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from agentforge.interfaces.vad.resource import VadWhisper
from agentforge.utils import logger

router = APIRouter()
vw = VadWhisper()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            response = await vw.process_chunk(data)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        vw.reset()
        # Attempt to close the WebSocket connection gracefully
        try:
            await websocket.close(code=1001)
        except Exception:
            # If there's an exception, it's likely the socket is already closed,
            # so we can ignore this exception.
            pass
