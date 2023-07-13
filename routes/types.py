from fastapi import APIRouter, Depends, HTTPException
from models import models, schemas
from typing import List 
import crud
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from auth.authenticate import authenticate

type_router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@type_router.get("/all", response_model = List[schemas.Type])
async def read_all_types(db : Session=Depends(get_db)):
    results = crud.get_all_types(db)
    return results

@type_router.get("/one/{typeId}", response_model = List[schemas.Type])
async def read_type(typeId:int,db:Session=Depends(get_db)):
    result = crud.get_type(db,typeId)
    if len(result)==0:
        raise HTTPException(status_code = 404, detail="Item not found")
    return result

@type_router.post("/new")
async def insert_type(Type: schemas.TypeCreate, db : Session=Depends(get_db), user:str = Depends(authenticate)):
    result = crud.insert_type(db,Type)
    return result

@type_router.put("/{typeId}",response_model = List[schemas.Type])
async def update_type(typeId:int, TypeUpdate: schemas.TypeUpdate, db: Session = Depends(get_db)):
    # 해당 id의 type이 없으면 에러
    if len(crud.get_type(db,typeId))==0:
        raise HTTPException(status_code = 404, detail="Item not found")
    else:
        updated_type = crud.update_type(db,typeId,TypeUpdate)
        return updated_type
    
@type_router.delete("/{typeId}")
async def del_type(typeId:int, TypeUpdate: schemas.TypeUpdate, db: Session = Depends(get_db)):
    # 해당 id의 type이 없으면 에러
    if len(crud.get_type(db,typeId))==0:
        raise HTTPException(status_code = 404, detail="Type not found")
    else:
        deleted_type = crud.del_type(db,typeId)
        return deleted_type
    
@type_router.get("/items/{typeId}",response_model = List[schemas.Corpus])
async def get_type_items(typeId:int, db:Session = Depends(get_db)):
    if len(crud.get_type(db,typeId)) == 0:
        raise HTTPException(status_code = 404, detail ="Type not found")
    else:
        items = crud.get_type_items(db,typeId)
        return items