from fastapi import APIRouter, Depends
from database.connection import SessionLocal
import crud
from typing import List
from models import models, schemas
from sqlalchemy.orm import Session

#authentication
from fastapi.security import OAuth2PasswordRequestForm

user_router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# create new user(signUp)
@user_router.post("/signup")
async def create_user(User: schemas.UserCreate, db : Session=Depends(get_db)):
    result = crud.create_user(db,User)
    return result

# get users
@user_router.get("/all",response_model = List[schemas.User])
async def get_users(db : Session=Depends(get_db)):
    result = crud.get_all_users(db)
    return result

# user sign in
# request body 아닌, form 형식으로 요청 필요
@user_router.post("/signin",response_model = schemas.TokenResponse)
async def sign_user_in(User:OAuth2PasswordRequestForm = Depends(), db : Session=Depends(get_db)) -> dict:    
    token = crud.sign_user_in(User,db)
    return token
    