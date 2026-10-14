import streamlit as st
import os
from sqlalchemy import text


from login_page import show_login_page, is_authenticated, handle_logout
from app import show_dashboard
from landing_page import show_landing_page

from backend.database import engine

st.set_page_config(
    page_icon="frontend/assets/gbi3_logo.png", 
    page_title="Green Box Intel", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

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
    
    if is_authenticated():
        
        if st.session_state.get("page") == "login":
            st.session_state.page = None 

        
        try:
            user_id = st.session_state.get("user_id")
            
            query = text("SELECT is_approved FROM profiles WHERE id = :id")
            with engine.connect() as conn:
                result = conn.execute(query, {"id": user_id}).mappings().first()

            if result:
                approved = result.get("is_approved", False)
            else:
                approved = False
 
            if approved:
                show_dashboard()
            else:
                
                st.write("") 
                st.title("Green Box Intel")
                st.info("🕒 **Account Pending Verification**")
                st.write("We are currently verifying your credentials. You will receive an email once your secure workspace is activated.")
                
                handle_logout() 

        except Exception as e:
            st.error(f"Authentication Error: {e}")
            handle_logout()

    elif st.session_state.get("page") == "login":
        show_login_page()
    
    else:
        show_landing_page()

if __name__ == "__main__":
    main()