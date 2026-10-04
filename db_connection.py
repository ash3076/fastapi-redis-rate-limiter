from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine 
from dotenv import load_dotenv
import os 


load_dotenv()

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)

sessionLocal = sessionmaker(engine , autocommit = False , autoflush = False )