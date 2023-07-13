from sqlalchemy.orm import Mapped,relationship, mapped_column 
from sqlalchemy import ForeignKey, String, Integer
from typing import Optional, List
from database.connection import Base

#[META DATA] - async SQL Databases


#[DECLARATIVE MAPPING]
#Declarative Mapping + annotation
class Type(Base):
    __tablename__ = "CorpusTypes"

    typeId: Mapped[int] = mapped_column(Integer, primary_key=True)
    type : Mapped[str] = mapped_column(String(255), nullable=False)

    corpuses: Mapped[List["Corpus"]] = relationship(
        back_populates="category",
        cascade = "all, delete",
    )

# Declarative Mapping + annotation
class Corpus(Base):
    __tablename__ = "Corpuses"

    corpusId : Mapped[int] = mapped_column(Integer, primary_key=True) 
    typeId : Mapped[int] = mapped_column(Integer, ForeignKey("CorpusTypes.typeId"))
    content : Mapped[str]
    source : Mapped[str]
    source_detail : Mapped[Optional[str]] 

    category: Mapped["Type"] = relationship(back_populates="corpuses")

    

class User(Base):
    __tablename__ = "Users"

    userId: Mapped[int] = mapped_column(Integer, primary_key=True)
    email : Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password : Mapped[str] = mapped_column(String(255), nullable=False)
