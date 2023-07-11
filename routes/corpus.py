from fastapi import APIRouter, Depends, HTTPException
from models import models, schemas
from typing import List 
import crud
from sqlalchemy.orm import Session
from database.connection import SessionLocal

corpus_router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# insert item
@corpus_router.post("/new")
async def insert_item(Corpus: schemas.CorpusCreate, db : Session=Depends(get_db)):
    result = crud.insert_item(db,Corpus)
    return result

# get all items
@corpus_router.get("/all",response_model = List[schemas.Corpus])
async def read_all_items(db: Session = Depends(get_db)):
    items = crud.get_all_items(db)
    return items

# result retrun 값이 list 안에 담겨져서 오기 때문에 response_model = List[]로 지정
@corpus_router.get("/one/{id}",response_model = List[schemas.Corpus])
async def read_item(id:int, db: Session = Depends(get_db)):
    item = crud.get_item(db,id)
    if len(item)==0:
        raise HTTPException(status_code = 404, detail="Item not found")
    return item

# update item 
@corpus_router.put("/{id}",response_model = List[schemas.Corpus])
async def update_item(id:int, CorpusUpate: schemas.CorpusUpdate, db: Session = Depends(get_db)):
    updated_item = crud.update_item(db,id,CorpusUpate)
    
    return updated_item

# delete item
@corpus_router.delete("/{corpusId}")
async def del_item(corpusId:int, db:Session = Depends(get_db)):
    if len(crud.get_item(db,corpusId) == 0):
        raise HTTPException(status_code = 404, detail="Item not found")
    else:
        deleted_item = crud.del_item(db,corpusId)
        return deleted_item



