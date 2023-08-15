# bot/database/models.py:
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, Sequence('car_id_seq'), primary_key=True)
    link = Column(String(500), unique=True)
