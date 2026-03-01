import os
from supabase import create_client, Client
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

@st.cache_resource
def init_connection() -> Client:
    url = os.getenv("SUPABASE_URL")
    # Make sure this matches the exact string in your .env file
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    # Debug print (removes this after it works!)
    if not key:
        print("DEBUG: SUPABASE_SERVICE_ROLE_KEY is None! Check your .env file.")
    
    if not url or not key:
        st.error("Supabase URL or Service Role Key missing!")
        st.stop()
        
    return create_client(url, key)

supabase = init_connection()

class DatabaseManager:
    def __init__(self):
        self.client = supabase

    # --- USER & QUOTA LOGIC ---
    def get_user_profile(self, user_id: str):
        """Fetches the user's remaining page quota safely."""
        # Remove .single() so it doesn't crash on empty results
        res = self.client.table("profiles").select("*").eq("id", user_id).execute()
        
        # If the list is empty, return None
        if not res.data:
            return None
            
        # Return the first matching row
        return res.data[0]

    def update_user_quota(self, user_id: str, pages_processed: int):
        """Subtracts pages from the user's limit."""
        profile = self.get_user_profile(user_id)
        
        # Safety check: Only do the math if the profile actually exists
        if profile:
            # Safely grab the quota, defaulting to 0 if something is weird
            current_quota = profile.get('remaining_quota', 0)
            
            # Calculate new quota and prevent it from going into negative numbers
            new_quota = max(0, current_quota - pages_processed)
            
            # Update Supabase
            self.client.table("profiles").update({"remaining_quota": new_quota}).eq("id", user_id).execute()
            
            print(f"📉 SUCCESS: Deducted {pages_processed} pages. User {user_id} now has {new_quota} pages left.")
        else:
            print(f"⚠️ Failed to deduct quota: No profile found for user {user_id}")

    def save_case(self, user_id: str, job_id: str, case_name: str, chronology: str, total_pages: int, metadata: dict):
        """Saves or Updates the main case analysis in the 'cases' table."""
        data = {
            "id": job_id,
            "user_id": user_id,
            "case_name": case_name,
            "chronology_text": chronology,
            "total_pages": total_pages, # Matches the argument name and Supabase column
            "metadata": metadata  
        }
        return self.client.table("cases").upsert(data).execute()

    def save_document(self, case_id: str, file_name: str, page_count: int):
        """Adds a record for an individual file to the 'documents' table."""
        doc_data = {
            "case_id": case_id,
            "file_name": file_name,
            "page_count": page_count
        }
        return self.client.table("documents").insert(doc_data).execute()

    def get_all_cases(self, user_id: str):
        """Fetches all cases for the sidebar."""
        res = self.client.table("cases").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        # Convert list to dict to match your existing frontend logic
        return {item['id']: item for item in res.data}

    def delete_case(self, job_id: str):
        """Deletes all documents first, then the case itself."""
        # 1. Delete associated documents
        self.client.table("documents").delete().eq("case_id", job_id).execute()
        """Removes a case from the DB."""
        return self.client.table("cases").delete().eq("id", job_id).eq("user_id", user_id).execute()
    
    def has_enough_quota(self, user_id: str, required_pages: int) -> bool:
        """Checks if the user has enough page quota left to process the request."""
        try:
            profile = self.get_user_profile(user_id)
            
            if not profile:
                print(f"⚠️ No profile found for user {user_id}")
                return False
                
            # 1. ADD THIS TO SEE THE EXACT COLUMNS SUPABASE RETURNED 👇
            print(f"🔍 DEBUG PROFILE DATA: {profile}") 
            
            remaining_quota = profile.get("remaining_quota", 0) 
            
            # 2. ADD THIS TO SEE THE MATH 👇
            print(f"🔍 DEBUG MATH: Has {remaining_quota} pages, Needs {required_pages} pages")
            
            return remaining_quota >= required_pages
            
        except Exception as e:
            print(f"❌ Error checking quota: {e}")
            return False