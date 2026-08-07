import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 1. Force Python to load the .env file FIRST
load_dotenv()
db_url = os.getenv("DATABASE_URL")

if not db_url:
    print("Error: Could not find DATABASE_URL in .env file!")
else:
    # 2. Connect directly to AWS and wipe the empty tables
    engine = create_engine(db_url)
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS documents CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS cases CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS profiles CASCADE;"))
    print("Tables dropped successfully! You are ready to run Streamlit.")