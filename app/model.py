from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    expire_date = Column(DateTime)
    api_key = Column(String, unique=True)