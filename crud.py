from fastapi import HTTPException
from database.connection import engine
from models import models, schemas
from sqlalchemy import text
from sqlalchemy.orm import Session

# ITEM CRUD

# create an item
def insert_item(db:Session,Corpus:schemas.CorpusCreate):
    db_corpus = models.Corpus (
        typeId = Corpus.typeId,
        content = Corpus.content,
        source = Corpus.source,
        source_detail = Corpus.source_detail
    ) 
    db.add(db_corpus)
    db.commit()
    db.refresh(db_corpus)
    
    return db_corpus
        
# get all items 
def get_all_items(db:Session):
    stmt = "SELECT Cor.corpusId, Cor.typeId, Type.type, Cor.content, Cor.source, Cor.source_detail FROM corpuses as Cor INNER JOIN CorpusTypes as Type ON Cor.typeId = Type.typeId ;"
    result = db.execute(text(stmt)).fetchall()
    return result

# get an item
def get_item(db:Session,id:int):
    stmt = "SELECT corpusId, typeId, content, source, source_detail FROM Corpuses WHERE corpusId = :corpusId"
    result = db.execute(text(stmt),{"corpusId":id}).fetchall()
    return result

#update an item 
def update_item(db:Session, id:int , CorpusUpdate : schemas.CorpusUpdate):
    stmt = "UPDATE Corpuses SET typeId = :typeId, content = :content, source = :source, source_detail = :source_detail WHERE corpusId = :id"
    db.execute(text(stmt),{"typeId":CorpusUpdate.typeId, "content":CorpusUpdate.content,
    "source":CorpusUpdate.source, "source_detail":CorpusUpdate.source_detail,"id":id})
    db.commit()

    result = get_item(db,id)
    return result

#delete an item
def del_item(db:Session, corpusId:int):
    if len(get_item(db,corpusId)) == 0 :
        return { "error":"There's no item for supplied id"}
    stmt = "DELETE FROM Corpuses WHERE corpusId = :corpusId"
    db.execute(text(stmt),{"corpusId":corpusId})
    db.commit()

    return {"msg":"item delete successfully"}

# create item - 에러 : add 대신 execute로 실행시, Instance '<Corpus at 0x103c0b760>' is not persistent within this Session 에러
# def insert_item(db:Session,Corpus:schemas.CorpusCreate):
#     db_corpus = models.Corpus (
#         typeId = Corpus.typeId,
#         content = Corpus.content,
#         source = Corpus.source,
#         source_detail = Corpus.source_detail
#     ) 
#     stmt = "INSERT INTO Corpuses (typeId, content, source, source_detail) VALUES (:typeId, :content, :source, :source_detail)"
#     db.execute(text(stmt),{"typeId":Corpus.typeId,"content":Corpus.content,"source":Corpus.source,"source_detail":Corpus.source_detail})
#     db.commit()
#     db.refresh(db_corpus)
#     return db_corpus

# TYPE CRUD

# get all types
def get_all_types(db:Session):
    stmt = "SELECT Cor.content, Cor.typeId, Cor.source, Cor.source_detail , Type.type FROM corpuses as Cor INNER JOIN CorpusTypes as Type ON Cor.typeId = Type.typeId  ;"
    result = db.execute(text(stmt)).fetchall()
    return result

# get an type
def get_type(db:Session,typeId:int):
    stmt = "SELECT typeId, type FROM CorpusTypes WHERE typeId = :typeId"
    result = db.execute(text(stmt),{"typeId":typeId}).fetchall()
    return result

# insert an type
def insert_type(db:Session,Type:schemas.TypeCreate):
    db_type = models.Type (
        type = Type.type
    ) 
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    
    return db_type 

# update an type
def update_type(db:Session, typeId:int , TypeUpdate : schemas.TypeUpdate):
    stmt = "UPDATE CorpusTypes SET type = :type WHERE typeId = :typeId"
    db.execute(text(stmt),{"type":TypeUpdate.type, "typeId":typeId})
    db.commit()
    result = get_type(db,typeId)
    return result

# delete an type
def del_type(db:Session, typeId:int):
    stmt = "SELECT * FROM Corpuses WHERE typeId = :typeId"
    child_data = db.execute(text(stmt),{"typeId":typeId}).fetchall()
    child_cnt = len(child_data)
    print(child_cnt)
    if child_cnt == 0:
        stmt = "DELETE FROM CorpusTypes WHERE typeId = :typeId"
        db.execute(text(stmt),{"typeId":typeId})
        db.commit()
        return {"msg":"type delete successfully"}
    else:
        msg = str(child_cnt)+"개의 관련 데이터가 존재합니다. 관련 데이터를 먼저 삭제해주세요."
        raise HTTPException(status_code = 404, detail=msg)

# get all items with specific typefa
def get_type_items(db:Session, typeId:int):
    stmt = "SELECT Cor.corpusId, Cor.content, Cor.source, Cor.source_detail, Cor.typeId, Type.type FROM Corpuses as Cor INNER JOIN CorpusTypes as Type ON Cor.typeId = Type.typeId WHERE Cor.typeId=:typeId"
    result = db.execute(text(stmt),{"typeId":typeId}).fetchall()
    return result

    

    