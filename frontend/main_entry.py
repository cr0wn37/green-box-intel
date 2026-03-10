import streamlit as st
from login_page import show_login_page, is_authenticated, handle_logout
from app import show_dashboard
from landing_page import show_landing_page

st.set_page_config(page_icon="frontend/assets/gbi3_logo.png", page_title="Green Box Intel", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* 1. Hide the footer and all Streamlit branding */
    footer {display: none !important;}
    [data-testid="stFooter"] {display: none !important;}
    .viewerBadge_container__1QSob {display: none !important;}
    .styles_viewerBadge__1yB_V {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}

    /* 2. Make the header transparent so the sidebar arrow SURVIVES */
    header {background-color: transparent !important; box-shadow: none !important;}
    [data-testid="stHeader"] {background-color: transparent !important;}

    /* 3. Hide the colored decoration line at the very top */
    [data-testid="stDecoration"] {display: none !important;}

    /* 4. Hide the hamburger menu and developer tools (but keep the arrow) */
    #MainMenu {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}

    /* 5. Adjust padding to remove empty footer space */
    .main .block-container {
        padding-top: 3rem !important; 
        padding-bottom: 0rem !important;
    }
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