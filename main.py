from fastapi import FastAPI, Response, Request
from starlette.background import BackgroundTask
from starlette.types import Message
import uvicorn # ASGI server(비동기 web server)
import logging # logging
from pathlib import Path
from custom_logging import CustomizeLogger

from routes import corpus, types, users, files


# logger 인스턴스 생성
logger = logging.getLogger("main")

config_path = Path(__file__).with_name("logging_config.json")

def create_app() -> FastAPI:
    app = FastAPI(title='HyundaiRB BackEnd')
    logger = CustomizeLogger.make_logger(config_path)
    app.logger = logger

    return app

app = create_app()

#routers
app.include_router(corpus.corpus_router, prefix='/corpus')
app.include_router(types.type_router, prefix='/type')
app.include_router(users.user_router, prefix='/user')
app.include_router(files.file_router, prefix='/file')

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)
