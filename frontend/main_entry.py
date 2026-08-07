import streamlit as st
import os
from sqlalchemy import text

# Import your routing functions
from login_page import show_login_page, is_authenticated, handle_logout
from app import show_dashboard
from landing_page import show_landing_page

# Import the new AWS engine instead of supabase
from backend.database import engine

st.set_page_config(
    page_icon="frontend/assets/gbi3_logo.png", 
    page_title="Green Box Intel", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Hide Streamlit styling
hide_streamlit_style = """
    <style>
    footer {visibility: hidden !important;}
    [data-testid="stDecoration"] {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "landing"

def main():
    # 1. Check authentication FIRST
    if is_authenticated():
        # Clear the 'page' state to avoid conflicts
        if st.session_state.get("page") == "login":
            st.session_state.page = None 

        # --- GATEKEEPER: Check if Admin has approved this user ---
        try:
            user_id = st.session_state.get("user_id")
            
            # 1. Query the new AWS Postgres database for approval status
            query = text("SELECT is_approved FROM profiles WHERE id = :id")
            with engine.connect() as conn:
                result = conn.execute(query, {"id": user_id}).mappings().first()

            # 2. Check if the user record exists and grab their status
            if result:
                approved = result.get("is_approved", False)
            else:
                approved = False
 
            # 3. Direct the user based on approval
            if approved:
                show_dashboard()
            else:
                # Minimalist Pending State
                st.write("") 
                st.title("Green Box Intel")
                st.info("🕒 **Account Pending Verification**")
                st.write("We are currently verifying your credentials. You will receive an email once your secure workspace is activated.")
                
                handle_logout() 

        except Exception as e:
            st.error(f"Authentication Error: {e}")
            handle_logout()

    # 2. Handle routing for unauthenticated users
    elif st.session_state.get("page") == "login":
        show_login_page()
    
    else:
        show_landing_page()

if __name__ == "__main__":
    main()