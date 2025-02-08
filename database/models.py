from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    registered_at = Column(DateTime, default=datetime.now)
    is_known = Column(Boolean, default=False)
