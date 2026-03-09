import streamlit as st
from login_page import show_login_page, is_authenticated, handle_logout
from app import show_dashboard
from landing_page import show_landing_page

st.set_page_config(page_icon="frontend/assets/gbi3_logo.png", page_title="Green Box Intel", layout="wide", initial_sidebar_state="expanded")

# Place this in main_entry.py
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    
    /* Made with Streamlit footer - multiple selectors */
    .reportview-container .main footer {visibility: hidden !important;}
    footer.css-1lsmgbg {display: none !important;}
    .css-1lsmgbg.egzxvld0 {display: none !important;}
    
    /* Fullscreen button */
    button[title="View fullscreen"] {display: none !important;}
    [data-testid="StyledFullScreenButton"] {display: none !important;}
    .stApp > header {display: none !important;}
    
    /* Bottom bar / toolbar */
    .stDeployButton {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    
    /* Remove bottom padding gap left behind */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    </style>
<script>
    // Remove Streamlit branding elements via JS
    const observer = new MutationObserver(function() {
        const footer = document.querySelector('footer');
        if (footer) footer.style.display = 'none';
        
        const toolbar = document.querySelector('[data-testid="stToolbar"]');
        if (toolbar) toolbar.style.display = 'none';
        
        const fullscreen = document.querySelectorAll('button[title="View fullscreen"]');
        fullscreen.forEach(btn => btn.style.display = 'none');
    });
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
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