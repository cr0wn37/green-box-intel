import streamlit as st
from login_page import show_login_page, is_authenticated, handle_logout
from app import show_dashboard
from landing_page import show_landing_page

st.set_page_config(page_icon="frontend/assets/gbi3_logo.png", page_title="Green Box Intel", layout="wide", initial_sidebar_state="expanded")

# Place this in main_entry.py
st.markdown("""
    <style>
    /* 1. Hide the standard elements inside your app */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* 2. Target the specific Streamlit Cloud badge class seen in your Inspect tool */
    [data-testid="stStatusWidget"], .viewerBadge_container__1QSob, .stAppDeployButton {
        display: none !important;
    }

    /* 3. THE FIX: Physically cover the bottom 50px of the screen */
    .footer-mask {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 50px;
        background-color: white; /* Matches your landing page */
        z-index: 999999;
    }
    </style>
    <div class="footer-mask"></div>
""", unsafe_allow_html=True)

def main():
    # 1. Check if user is already logged in via Supabase session
    if is_authenticated():
        # User is logged in, show the full dashboard
        show_dashboard()
        handle_logout() # Keeps the logout button in the sidebar
    
    # 2. If not logged in, check which public page they are on
    elif st.session_state.get("page") == "login":
        show_login_page()
    
    else:
        # Default view for new visitors
        show_landing_page()

if __name__ == "__main__":
    main()