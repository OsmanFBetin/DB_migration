from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)
Base = declarative_base()

def get_database():
    return database

def get_engine():
    return engine
