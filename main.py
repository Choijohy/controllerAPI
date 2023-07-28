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

#logging for body data
def log_info(req_body,res_body):
    # `Response_body` was bytes type
    if isinstance(res_body,bytes):
        res_body = "image bytes data"
        
    logging.info("Req"+req_body)
    logging.info("Res"+res_body)

async def set_body(request: Request, body:bytes):
    async def receive() -> Message:
        return {'type':'http.request','body':body}
    request._receive = receive

# logging middelware
@app.middleware('http')
async def body_logging(request: Request, call_next):
    # request.body(): get body as bytes type
    req_body = await request.body()
    await set_body(request,req_body)
    
    response = await call_next(request)
    
    # initialize an empty binary obj(bytes)
    res_body = b''
    # concatenate all the data chunks received 
    async for chunk in response.body_iterator:
        res_body += chunk

    # req_body가 multipart/form-data
    if 'content-type' in request.headers:
        if request.headers['content-type'].startswith('multipart'):
            req_body = 'image bytes data'
        else:
            req_body = req_body.decode('utf-8')

    try:
        # `response_body` was a json format. convert bytes to string
        res_body = res_body.decode('utf-8')
        task = BackgroundTask(log_info,req_body,res_body)
    except :
        # `response_body` was not a json format. (i.e. img, ...)
        task = BackgroundTask(log_info, req_body, res_body)
 
    return Response(content=res_body, status_code = response.status_code,
    headers=dict(response.headers),media_type=response.media_type, background=task)

#routers
app.include_router(corpus.corpus_router, prefix='/corpus')
app.include_router(types.type_router, prefix='/type')
app.include_router(users.user_router, prefix='/user')
app.include_router(files.file_router, prefix='/file')

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)
