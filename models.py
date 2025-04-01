from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Text

Base = declarative_base()

class User(Base):
    __tablename__ = "test_users"
    id = Column(Integer, primary_key=True)
    name = Column(Text)