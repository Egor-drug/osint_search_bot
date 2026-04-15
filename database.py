from sqlalchemy import create_engine, String, Integer, Column, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

# Берем DATABASE_URL из переменных окружения Render
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    raise Exception("DATABASE_URL environment variable not set!")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    register_at = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    premium = Column(Boolean, default=False)
    queries = Column(Integer, default=0)

class BroadCast(Base):
    __tablename__ = 'broadcasts'
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    sent_at = Column(DateTime, default=datetime.datetime.now())

# Создаём таблицы при старте
Base.metadata.create_all(bind=engine)
