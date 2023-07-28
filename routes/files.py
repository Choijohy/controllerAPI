# fastAPI의 UploadFile, FileResponse 객체 활용
# DB아닌 저장경로를 통해, 파일 저장 및 불러오기

from fastapi import APIRouter,  UploadFile, Query, HTTPException, status
from typing_extensions import Annotated
from fastapi.responses import FileResponse
from typing import Union
import os 

file_router = APIRouter()

# 파일 업로드
@file_router.post("/image")
async def create_upload_file(file: Union[UploadFile,None]=None):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No file to be uploaded"
        )
    else:
        # 업로드 url 적절하게 수정
        UPLOAD_DIR = '/Users/jiheechoi/Desktop/FastAPI_SQL/planner/files'
        content = await file.read()
        file_location = os.path.join(UPLOAD_DIR,file.filename)
        # w - 쓰기모드, b - 바이너리 모드(비트단위 데이터 기록) 
        # b 모드가 없으면 이미지 파일은 TypeError
        with open(file_location, "wb") as file_object:
            file_object.write(content)

        return {
            "filename": file.filename,
            "path" : UPLOAD_DIR,
            "type" : file.content_type}

# 파일 다운로드
# query string : file_path is required when request
@file_router.get("/image")
async def download_file(file_path: Union[str, None] = Query(default=None)):
    if not file_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No path provided"
        )
    elif not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="file path does not exist"
        )
    else:
        return FileResponse(file_path)
       
            