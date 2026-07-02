import streamlit as st
from login_page import show_login_page, is_authenticated, handle_logout
from app import show_dashboard
from landing_page import show_landing_page
from backend.database import supabase
import os

if "page" not in st.session_state:
    st.session_state.page = "landing"

st.set_page_config(page_icon="frontend/assets/gbi3_logo.png", page_title="Green Box Intel", layout="wide", initial_sidebar_state="expanded")

css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
with open(css_path) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



def main():
    # 1. Check authentication FIRST
    if is_authenticated():
        # Clear the 'page' state to avoid conflicts
        if st.session_state.get("page") == "login":
            st.session_state.page = None 

        # --- GATEKEEPER: Check if Admin has approved this user ---
        # --- GATEKEEPER: Check if Admin has approved this user ---
        try:
            user_id = st.session_state.get("user_id")
            
            # 1. Drop .single() so it returns an empty list instead of crashing
            res = supabase.table("profiles").select("is_approved").eq("id", user_id).execute()

           
            # 2. Check if the user record actually exists in the table
            if res.data and len(res.data) > 0:
                # User exists, pull their approval status
                approved = res.data[0].get("is_approved", False)
            else:
                # User does not exist in profiles table yet
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
            st.error(f"Actual Python Error: {e}")
            handle_logout()

    # 2. Handle routing for unauthenticated users
    elif st.session_state.get("page") == "login":
        show_login_page()
    
    else:
        show_landing_page()

if __name__ == "__main__":
    main()