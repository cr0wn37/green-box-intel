import os
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

def init_engine():
    """Initializes the standard SQLAlchemy connection engine for AWS RDS."""
    db_url = os.getenv("DATABASE_URL")
    
    if not db_url:
        print("CRITICAL ERROR: DATABASE_URL missing from Environment Variables!")
        raise ValueError("Missing database configuration credentials")
        
    # pool_pre_ping=True forces SQLAlchemy to test the connection before using it.
    # This is critical for Streamlit apps so connections don't time out overnight.
    return create_engine(db_url, pool_pre_ping=True)

# Initialize the global engine instance
engine = init_engine()

def create_tables_if_not_exists():
    """Automatically creates the required tables on AWS RDS if they don't exist."""
    print("Checking and initializing database schema on AWS RDS...")
    
    schema_sql = """
    CREATE TABLE IF NOT EXISTS profiles (
        id VARCHAR(255) PRIMARY KEY,
        email VARCHAR(255) UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        remaining_quota INT DEFAULT 100,
        is_approved BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS cases (
        id VARCHAR(255) PRIMARY KEY,
        user_id VARCHAR(255) REFERENCES profiles(id) ON DELETE SET NULL,
        case_name VARCHAR(255) NOT NULL,
        chronology_text TEXT,
        total_pages INT DEFAULT 0,
        metadata JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        case_id VARCHAR(255) REFERENCES cases(id) ON DELETE CASCADE,
        file_name VARCHAR(255) NOT NULL,
        s3_url TEXT,
        page_count INT DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    with engine.begin() as conn:
        conn.execute(text(schema_sql))
    print("Database schema synchronization complete!")

# Run the schema generation immediately when backend loads
create_tables_if_not_exists()


class DatabaseManager:
    def __init__(self):
        self.engine = engine

    # --- USER & QUOTA LOGIC ---
    def get_user_profile(self, user_id: str):
        """Fetches the user's remaining page quota safely."""
        query = text("SELECT * FROM profiles WHERE id = :id")
        with self.engine.connect() as conn:
            result = conn.execute(query, {"id": user_id})
            row = result.mappings().first()
            return dict(row) if row else None

    def update_user_quota(self, user_id: str, pages_processed: int):
        """Subtracts pages from the user's limit."""
        profile = self.get_user_profile(user_id)
        
        if profile:
            current_quota = profile.get('remaining_quota', 0)
            new_quota = max(0, current_quota - pages_processed)
            
            query = text("UPDATE profiles SET remaining_quota = :quota WHERE id = :id")
            with self.engine.begin() as conn:
                conn.execute(query, {"quota": new_quota, "id": user_id})
                
            print(f"📉 SUCCESS: Deducted {pages_processed} pages. User {user_id} now has {new_quota} pages left.")
        else:
            print(f"⚠️ Failed to deduct quota: No profile found for user {user_id}")

    def save_case(self, user_id: str, job_id: str, case_name: str, chronology: str, total_pages: int, metadata: dict):
        """Saves or Updates the main case analysis using PostgreSQL Upsert syntax."""
        query = text("""
            INSERT INTO cases (id, user_id, case_name, chronology_text, total_pages, metadata)
            VALUES (:id, :user_id, :case_name, :chronology_text, :total_pages, :metadata)
            ON CONFLICT (id) DO UPDATE SET
                user_id = EXCLUDED.user_id,
                case_name = EXCLUDED.case_name,
                chronology_text = EXCLUDED.chronology_text,
                total_pages = EXCLUDED.total_pages,
                metadata = EXCLUDED.metadata
        """)
        
        with self.engine.begin() as conn:
            conn.execute(query, {
                "id": job_id,
                "user_id": user_id,
                "case_name": case_name,
                "chronology_text": chronology,
                "total_pages": total_pages,
                "metadata": json.dumps(metadata) # Direct JSON serialization for PG JSONB
            })

    def save_document(self, case_id: str, file_name: str, page_count: int):
        """Adds a record for an individual file to the 'documents' table."""
        query = text("""
            INSERT INTO documents (case_id, file_name, page_count)
            VALUES (:case_id, :file_name, :page_count)
        """)
        with self.engine.begin() as conn:
            conn.execute(query, {
                "case_id": case_id,
                "file_name": file_name,
                "page_count": page_count
            })

    def get_all_cases(self, user_id: str):
        """Fetches all cases ordered by newest first, returned as a dictionary matching frontend expectations."""
        query = text("SELECT * FROM cases WHERE user_id = :user_id ORDER BY created_at DESC")
        with self.engine.connect() as conn:
            result = conn.execute(query, {"user_id": user_id})
            rows = result.mappings().fetchall()
            # Returns data structure identical to Supabase's format
            return {item['id']: dict(item) for item in rows}

    def get_documents_by_case(self, case_id: str):
        """Fetches all documents associated with a specific case from AWS."""
        query = text("SELECT * FROM documents WHERE case_id = :case_id ORDER BY created_at ASC")
        with self.engine.connect() as conn:
            result = conn.execute(query, {"case_id": case_id})
            # Convert the SQLAlchemy result rows into standard Python dictionaries
            return [dict(row) for row in result.mappings().fetchall()]

    def delete_case(self, job_id: str):
        """Safely removes associated documents first due to foreign keys, then deletes the case."""
        with self.engine.begin() as conn:
            conn.execute(text("DELETE FROM documents WHERE case_id = :case_id"), {"case_id": job_id})
            conn.execute(text("DELETE FROM cases WHERE id = :id"), {"id": job_id})
    
    def has_enough_quota(self, user_id: str, required_pages: int) -> bool:
        """Checks if the user has enough page quota left to process the request."""
        try:
            profile = self.get_user_profile(user_id)
            if not profile:
                print(f"⚠️ No profile found for user {user_id}")
                return False
                
            print(f"🔍 DEBUG PROFILE DATA: {profile}") 
            remaining_quota = profile.get("remaining_quota", 0) 
            print(f"🔍 DEBUG MATH: Has {remaining_quota} pages, Needs {required_pages} pages")
            
            return remaining_quota >= required_pages
            
        except Exception as e:
            print(f"❌ Error checking quota: {e}")
            return False