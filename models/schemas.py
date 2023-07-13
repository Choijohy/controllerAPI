from typing import List, Union

from pydantic import BaseModel

# pydantic 모델(=schema) : db와 맵핑 및 연동되기 위한 obj 역할을 하는 sqlAlchemy의 model과 달리, 데이터를 읽어들여오고, 쓸때 사용되는 모델

# type base
class TypeBase(BaseModel):
    type: str

class TypeCreate(TypeBase):
    pass

# type schema : update
class TypeUpdate(BaseModel):
    type : Union[str, None] = None

# type schema : read
class Type(TypeBase):
    typeId : int
    class Config:
            orm_mode = True

# corpus base
class CorpusBase(BaseModel):
    typeId : int
    content : str
    source : str
    # string or none 
    source_detail : Union[str,None] = None

# corpus schema : create
class CorpusCreate(CorpusBase):
    pass

# corpus schema : read
class Corpus(CorpusBase):
    corpusId : str
    type : str
    class Config:
        orm_mode = True

# corpus schema : update
class CorpusUpdate(BaseModel):
    content : Union[str, None] = None
    source : Union[str, None] = None
    source_detail : Union[str , None] = None

# user base
class UserBase(BaseModel):
    email : str

# user schema : create
class UserCreate(UserBase):
    password : str

# user schema : read
class User(UserBase):
    userId : int
    class Config:
        orm_mode = True

# user schema : update
class UserUpdate(UserBase):
    email : Union[str, None] = None
    password : Union[str, None] = None

# token schema : read
class TokenResponse(BaseModel):
    access_token : str
    token_type : str