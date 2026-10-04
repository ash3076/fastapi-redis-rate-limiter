# from pydantic import BaseModel
from sqlalchemy.orm import declarative_base 
from sqlalchemy import Column , Integer , String 

Base = declarative_base()


class Register(Base):
    __tablename__ = "registerTable"

    id = Column(Integer,  primary_key = True , index = True , autoincrement=True)
    username = Column(String  , unique = True )
    password = Column(String)