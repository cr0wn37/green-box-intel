import streamlit as st
from login_page import show_login_page, is_authenticated, handle_logout
from app import show_dashboard
from landing_page import show_landing_page

if "page" not in st.session_state:
    st.session_state.page = "landing"

st.set_page_config(page_icon="frontend/assets/gbi3_logo.png", page_title="Green Box Intel", layout="wide", initial_sidebar_state="expanded")



def main():
    # 1. Check authentication FIRST
    if is_authenticated():
        # Clear the 'page' state to avoid conflicts
        if st.session_state.get("page") == "login":
            st.session_state.page = None 

        # --- GATEKEEPER: Check if Admin has approved this user ---
        try:
            user_id = st.session_state.get("user_id")
            res = supabase.table("profiles").select("is_approved").eq("id", user_id).single().execute()
            
            # Simple True/False check
            approved = res.data.get("is_approved", False) if res.data else False

            if approved:
                show_dashboard()
            else:
                # Minimalist Pending State
                st.write("") 
                st.title("Green Box Intel")
                st.info("🕒 **Account Pending Verification**")
                st.write("We are currently verifying your credentials. You will receive an email once your secure workspace is activated.")
                
            handle_logout() 

        except Exception:
            st.error("Connection error. Please refresh the page.")
            handle_logout()

    # 2. Handle routing for unauthenticated users
    elif st.session_state.get("page") == "login":
        show_login_page()
    
    else:
        show_landing_page()

if __name__ == "__main__":
    main()