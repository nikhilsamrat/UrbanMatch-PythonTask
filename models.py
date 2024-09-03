from sqlalchemy import Column, INTEGER, TEXT
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(INTEGER, primary_key=True, index=True)
    name = Column(TEXT, index=True)
    age = Column(INTEGER)
    gender = Column(TEXT)
    email = Column(TEXT, unique=True, index=True)
    city = Column(TEXT, index=True)
    interests = Column(TEXT)
