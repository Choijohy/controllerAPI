# JWT 문자열 인코딩, 디코딩 
import time
from datetime import datetime

from fastapi import HTTPException, status
from jose import jwt, JWTError

from dotenv import load_dotenv
import os

# import .env
load_dotenv()

jwt_key = os.getenv("JWT_SECRET_KEY")


# 토근 생성
def create_access_token(user: str):
    payload = {
        "user":user, # userId
        "expires":time.time() + 3600 # to be expired in an hour
    }
    # encode(payload, key to sign payload, algorithm)
    token = jwt.encode(payload, jwt_key, algorithm="HS256")
    return token

# 토근 검증
def verify_access_token(token:str):
    try:
        data = jwt.decode(token,jwt_key,algorithms=["HS256"])
        expire = data.get("expires")

        # 유효하지 않은 토큰
        if expire is None:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "No Access token supplied"
            )
        # 만료 토큰
        if datetime.utcnow() > datetime.utcfromtimestamp(expire):
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detial = "Token expired"
            )
        return data
    
    except JWTError:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detial = "Invalid token"
        )