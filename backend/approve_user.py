import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
db_url = os.getenv("DATABASE_URL")

engine = create_engine(db_url)

with engine.begin() as conn:
    # This acts as an admin overriding the system to approve all pending accounts
    conn.execute(text("UPDATE profiles SET is_approved = TRUE;"))

print("✅ All users approved! You are ready to log into the dashboard.")