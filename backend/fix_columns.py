import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load the environment variables to get the database URL
load_dotenv()
db_url = os.getenv("DATABASE_URL")

if not db_url:
    print("Error: Could not find DATABASE_URL in .env file!")
else:
    engine = create_engine(db_url)
    
    # Use ALTER TABLE to forcefully inject the missing columns
    with engine.begin() as conn:
        try:
            conn.execute(text("ALTER TABLE profiles ADD COLUMN password_hash VARCHAR(255);"))
            print("✅ Added password_hash column!")
        except Exception as e:
            print(f"password_hash might already exist: {e}")
            
        try:
            conn.execute(text("ALTER TABLE profiles ADD COLUMN is_approved BOOLEAN DEFAULT FALSE;"))
            print("✅ Added is_approved column!")
        except Exception as e:
            print(f"is_approved might already exist: {e}")

    print("Database patching complete! You are ready to run Streamlit.")