# 패스워드 암호화 - 계정 등록, 로그인

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class HashPassword:
    #해싱값 반환
    def create_hash(self,password:str):
        return pwd_context.hash(password)
    
    # 일반 텍스트형 비밀번호와 해싱판 비밀번호가 두 값이 일치하는지 비교 - T/F 반환
    def verify_hash(self,plain_password:str, hashed_password:str):
        return pwd_context.verify(plain_password, hashed_password)