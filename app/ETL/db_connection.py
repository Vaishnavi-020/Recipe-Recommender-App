from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

database_url=os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL not found in .env file")

engine=create_engine(database_url)

with engine.connect() as conn:
    print('Connected to POSTGRESQL succesfully!')