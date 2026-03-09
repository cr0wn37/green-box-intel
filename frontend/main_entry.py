import streamlit as st
from login_page import show_login_page, is_authenticated, handle_logout
from app import show_dashboard
from landing_page import show_landing_page

st.set_page_config(page_icon="frontend/assets/gbi3_logo.png", page_title="Green Box Intel", layout="wide", initial_sidebar_state="expanded")

hide_st_style = """
    <style>
    /* 1. Hide the Main Menu, Header, and Footer */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* 2. Target the specific 'Built with Streamlit' bar in Community Cloud */
    .viewerBadge_container__1QSob {display: none !important;}
    .stAppDeployButton {display: none !important;}
    [data-testid="stStatusWidget"] {visibility: hidden !important;}

    /* 3. Aggressively hide the Fullscreen button on images/frames */
    [data-testid="stFullScreenFrame"] {display: none !important;}
    button[title="View fullscreen"] {visibility: hidden !important;}

    /* 4. Remove extra padding that might keep the footer area visible */
    .block-container {
        padding-bottom: 0rem !important;
    }
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

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