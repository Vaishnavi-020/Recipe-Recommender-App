import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

database_url = os.getenv("DATABASE_URL")

# Check whether the environment variable was loaded
assert database_url, "DATABASE_URL was not found!"

# Create the engine using .env
engine = create_engine(database_url)

# Test the connection and query the existing database
with engine.connect() as conn:
    result = conn.execute(
        text("SELECT COUNT(*) FROM recipes")
    )
    count = result.scalar()

    print("Database connection successful!")
    print("Recipes table row count:", count)

engine.dispose()