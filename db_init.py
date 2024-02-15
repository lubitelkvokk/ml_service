import sqlalchemy
from fastapi import FastAPI
from sqlalchemy import create_engine, DateTime, func, ForeignKey, Boolean, Float
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
import psycopg2
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./mydatabase.db"

# создание движка
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

Base = sqlalchemy.orm.declarative_base()  # определение модели

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()
