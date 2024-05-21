from fastapi import FastAPI, WebSocket, Cookie, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import logging
from typing import Optional
import uvicorn

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)  
logger.setLevel(logging.DEBUG)

app = FastAPI()
clients = {}

app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")

AUDIOBOOK_PATH = "./audiobook.mp3"
#CHUNK_SIZE = 1024 * 1024  # 1 MB
CHUNK_SIZE = 128 * 1024  # 1 MB

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/size")
async def audiobook_size():
    try:
        # Get the size of the file
        file_size = os.path.getsize(AUDIOBOOK_PATH)
        return {"file_size": file_size}
    except FileNotFoundError:
        # Handle the error if file is not found
        return {"error": "File not found."}
    except Exception as e:
        # Handle other potential errors
        return {"error": str(e)}

@app.get("/", response_class=HTMLResponse)
async def get_client(request: Request):
    logging.basicConfig(level=logging.DEBUG)
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/set", response_class=HTMLResponse)
async def get_client(request: Request):
    logging.basicConfig(level=logging.DEBUG)
    return templates.TemplateResponse("set.html", {"request": request})


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, last_position: Optional[int] = Cookie(default=0)):
    if client_id not in clients:
        # Initialize a new client session if not already present
        clients[client_id] = {"position": last_position, "websocket": websocket}
        logger.info(f"Client {client_id} connected, request to seek to {last_position}")
    else:
        # Update the existing client session with the new WebSocket connection
        clients[client_id]['websocket'] = websocket
        logger.info(f"Client {client_id} reconnected")


    try:                
        await websocket.accept()
        await websocket.send_text("ready")
        with open(AUDIOBOOK_PATH, "rb") as audio:
            audio.seek(last_position)
            while chunk := audio.read(CHUNK_SIZE):
                message = await websocket.receive_text()
                if (message) == "next":
                    logger.info(f"Client {client_id} requested next chunk. New position {clients[client_id]['position']}.")
                    await websocket.send_bytes(chunk)
                    clients[client_id]['position'] += len(chunk)
                elif "seek=" in message:
                    newpos = int(message.split('=')[1],10)
                    clients[client_id]['position'] = newpos
                    audio.seek(newpos)
                    logger.info(f"Client {client_id} requested seek to position {clients[client_id]['position']}.")
                else:
                    print(f"unexpected message {message}")
                #await websocket.send_text(f"set_cookie:{clients[client_id]['position']}")
        await websocket.close()
    except Exception as e:
        logger.error(f"Client {client_id} websocket error: {e}")
    finally:
        if client_id in clients[client_id]:
            del clients[client_id]

@app.get("/audiobook")
async def get_audiobook(last_position: int = Cookie(default=0)):
    response = FileResponse(AUDIOBOOK_PATH, media_type='audio/mpeg')
    response.set_cookie(key="last_position", value=str(last_position))
    return response

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run("main:app", host="127.0.0.1", port=8001, log_config=log_config, reload=True)
