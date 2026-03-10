import streamlit as st
from login_page import show_login_page, is_authenticated, handle_logout
from app import show_dashboard
from landing_page import show_landing_page

st.set_page_config(page_icon="frontend/assets/gbi3_logo.png", page_title="Green Box Intel", layout="wide", initial_sidebar_state="expanded")

hide_st_style = """
            <style>
            /* 1. Hide the footer branding */
            footer {visibility: hidden !important;}
            .viewerBadge_container__1QSob {display: none !important;}
            
            /* 2. MAKE HEADER TRANSPARENT (This brings back the sidebar button) */
            header {background-color: transparent !important;}
            [data-testid="stHeader"] {background-color: transparent !important;}
            
            /* 3. Hide the top decoration line */
            [data-testid="stDecoration"] {display: none !important;}
            
            /* 4. Hide menus and toolbars */
            #MainMenu {visibility: hidden !important;}
            [data-testid="stToolbar"] {visibility: hidden !important;}
            
            /* 5. BLOCK THE FULLSCREEN ESCAPE */
            button[title="View fullscreen"] {display: none !important;}
            [data-testid="StyledFullScreenButton"] {display: none !important;}
            
            /* 6. Fix the padding */
            .main .block-container {
                padding-top: 2rem !important;
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