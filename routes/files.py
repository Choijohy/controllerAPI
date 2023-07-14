# fastAPI의 UploadFile, FileResponse 객체 활용

from fastapi import APIRouter,  UploadFile, Query
from typing_extensions import Annotated
from fastapi.responses import FileResponse
from typing import Union
import os 

file_router = APIRouter()

# 파일 업로드
@file_router.post("/image")
async def create_upload_file(file: Union[UploadFile,None]=None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        UPLOAD_DIR = '/Users/jiheechoi/Desktop/FastAPI_SQL/planner/files'
        content = await file.read()
        file_location = os.path.join(UPLOAD_DIR,file.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(content)

        return {
            "filename": file.filename,
            "path" : UPLOAD_DIR,
            "type" : file.content_type}

# 파일 다운로드
# query string : image path is required when request
@file_router.get("/image")
async def download_file(path: Union[str, None] = Query(default=None)):
    if not path:
        return {"message":"No file to be downloaded"}
    else:
        return FileResponse('/'+path)