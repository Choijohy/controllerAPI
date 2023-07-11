from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
import sqlalchemy 

# import .env
load_dotenv()

# db url to be connected
SQLALCHEMY_DATABASE_URL = sqlalchemy.engine.URL.create(
    drivername="mysql",
    username=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=os.getenv("MYSQL_PORT"),
    database=os.getenv("MYSQL_DATABASE")
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



        
    