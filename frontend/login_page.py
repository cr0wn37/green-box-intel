import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import time
import sys


# Add the parent directory to Python's path so it can find the backend folder
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

# Now you can import from the backend folder!
from backend.database import supabase, DatabaseManager

def show_login_page():
    # Custom CSS for the login button (Updated to Green Box branding)
    st.markdown("""
        <style>
        /* Pill Button Override for Global Streamlit Buttons */
        div.stButton > button:first-child {
            background-color: #000000 !important; /* Pure black */
            color: #FFFFFF !important;            /* Pure white */
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-weight: 600;
            font-size: 0.95rem;
            padding: 0.6rem 2rem;                 /* Slightly more breathing room */
            border-radius: 999px;
            border: 1px solid #000000;            /* Sharp edges */
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            white-space: nowrap !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }

        div.stButton > button:hover {
            background-color: #1f2937 !important; /* Charcoal slate hover */
            border-color: #1f2937 !important;
            color: #FFFFFF !important;
            transform: translateY(-1px);          /* Subtle lift */
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
        }
        </style>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 14], vertical_alignment="center")
    
    with col1:
        st.image("frontend/assets/gbi2_logo.svg", width=70) # Adjust width as needed
        
    with col2:
        # Using HTML here removes the default heavy padding above st.title
        st.markdown("<h1 style='padding-top: 0rem; margin-bottom: 0px;'>Green Box Intel</h1>", unsafe_allow_html=True)
        
    # Place the caption right below the header
    st.caption("AI-Powered Medical Chronologies & Legal Analysis")

    st.write("")

    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    # --- LOGIN TAB ---
    with tab1:
        email = st.text_input("Email Address", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Log In"):
            if not email or not password:
                st.warning("Please enter both email and password.")
            else:
                try:
                    # 1. Authenticate with Supabase Auth
                    response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    
                    # 2. Store Session in Streamlit
                    st.session_state["user"] = response.user
                    st.session_state["user_id"] = response.user.id
                    st.session_state["access_token"] = response.session.access_token
                    
                    st.success("Welcome back! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Login failed: {str(e)}")

    # --- SIGN UP TAB ---
    with tab2:
        st.info("Start your 1500-page trial today.")
        new_email = st.text_input("Email Address", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_pass")
        
        if st.button("Create Account"):
            if not new_email or not new_password:
                st.warning("Please fill in all fields.")
            else:
                try:
                    # 1. Create Auth User
                    response = supabase.auth.sign_up({"email": new_email, "password": new_password})
                    
                    if response.user:
                        user_id = response.user.id
                        
                        # 2. Create Profile Entry (Quota) manually
                        # This ensures the 1500 limit is set immediately
                        try:
                            supabase.table("profiles").insert({
                                "id": user_id,
                                "email": new_email,
                                "remaining_quota": 1500
                            }).execute()
                        except Exception:
                            pass # Triggers might handle this automatically
                        
                        st.success("Account created! You can now log in.")
                    else:
                        st.warning("Check your email for a confirmation link.")
                        
                except Exception as e:
                    st.error(f"Sign up failed: {str(e)}")

def is_authenticated():
    """
    Returns True if user is logged in, False otherwise.
    """
    return "user" in st.session_state

def handle_logout():
    """
    Handles the 'Logout' button and clears the Supabase session.
    """
    with st.sidebar:
        st.divider()
        st.caption(f"Logged in as: {st.session_state['user'].email}")
        if st.button("Log Out"):
            supabase.auth.sign_out()
            # Clear everything to prevent 'app.py' from running logic on dead data
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()