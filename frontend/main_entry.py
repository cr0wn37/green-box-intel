import streamlit as st
from login_page import show_login_page, is_authenticated, handle_logout
from app import show_dashboard
from landing_page import show_landing_page

st.set_page_config(page_icon="frontend/assets/gbi3_logo.png", page_title="Green Box Intel", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* 1. Kill the Footer (Multiple Selectors) */
    footer {display: none !important; visibility: hidden !important;}
    [data-testid="stFooter"] {display: none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    .styles_viewerBadge__1yB_V {display: none !important;}
    
    /* 2. Bring Back the Sidebar Arrow */
    /* We make the header container transparent but NOT hidden */
    header {
        background-color: transparent !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* This specifically targets the Sidebar Toggle button */
    [data-testid="stSidebarCollapsedControl"] {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 50% !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        left: 10px !important;
        top: 10px !important;
        z-index: 999999 !important;
    }

    /* 3. Hide the rest of the junk */
    #MainMenu {visibility: hidden !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    [data-testid="stDecoration"] {display: none !important;}
    button[title="View fullscreen"] {display: none !important;}
    </style>
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