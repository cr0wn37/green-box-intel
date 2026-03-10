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
    # --- MODERN MONOCHROME CSS ---
    st.markdown("""
        <style>
        /* 1. Center the Logo and Headers inside the card */
        .centered-header {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        
        /* 2. Style the Tabs to be Black/Gray instead of Streamlit Pink */
        div[data-baseweb="tab-list"] {
            gap: 24px;
        }
        div[data-baseweb="tab"] {
            height: 50px;
            white-space: break-spaces;
            background-color: transparent !important;
        }
        div[data-baseweb="tab-highlight"] {
            background-color: #000000 !important; /* Black underline for active tab */
        }
        div[data-baseweb="tab"] p {
            color: #6b7280; /* Gray for inactive tabs */
            font-weight: 500;
        }
        div[aria-selected="true"] p {
            color: #000000 !important; /* Black text for active tab */
            font-weight: 600;
        }

        /* 3. Text Input Styling (Gray borders, black on focus) */
        div[data-baseweb="input"] {
            border-radius: 8px !important;
            border: 1px solid #e5e7eb !important;
            transition: all 0.2s;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #000000 !important; /* Black border on click */
            box-shadow: 0 0 0 1px #000000 !important;
        }

        /* 4. Pill Button Override (Your custom button) */
        div.stButton > button:first-child {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            font-weight: 600;
            border-radius: 999px;
            border: 1px solid #000000;
            transition: all 0.2s ease-in-out;
            width: 100%; /* Make button span full width of the card */
            margin-top: 10px;
        }
        div.stButton > button:hover {
            background-color: #374151 !important; /* Dark gray hover */
            border-color: #374151 !important;
            transform: translateY(-1px);
        }
        </style>
        """, unsafe_allow_html=True)

    # --- LAYOUT: 3 Columns to create a centered "Card" ---
    # The middle column (1.2) acts as the card width. The outer columns (1) are spacers.
    spacer_left, center_card, spacer_right = st.columns([1, 1.2, 1])

    with center_card:
        # Push the card down a bit from the top of the screen
        st.write("")
        st.write("")
        st.write("")
        
        # Wrap everything in a container to create the physical "Card" boundary
        with st.container(border=True):
            
            # --- CARD HEADER ---
            st.markdown("""
                <div class="centered-header">
                    <img src="frontend/assets/gbi3_logo.png" width="60" style="margin-bottom: 10px;">
                    <h2 style='padding-top: 0rem; margin-bottom: 0px; color: #111827;'>Green Box Intel</h2>
                    <p style='color: #6B7280; font-size: 0.9rem; margin-top: 5px;'>Secure Medical Chronologies</p>
                </div>
            """, unsafe_allow_html=True)

            # --- TABS ---
            tab1, tab2 = st.tabs(["Log In", "Create Account"])

            # --- LOGIN TAB ---
            with tab1:
                st.write("") # Subtle spacing
                email = st.text_input("Email Address", key="login_email", placeholder="attorney@lawfirm.com")
                password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
                
                if st.button("Sign In"):
                    if not email or not password:
                        st.error("Please enter both email and password.")
                    else:
                        with st.spinner("Authenticating..."):
                            try:
                                response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                                st.session_state["user"] = response.user
                                st.session_state["user_id"] = response.user.id
                                st.session_state["access_token"] = response.session.access_token
                                
                                st.success("Access granted. Redirecting...")
                                time.sleep(1)
                                st.rerun()
                            except Exception as e:
                                st.error("Invalid email or password.") # More professional than showing the raw error

            # --- SIGN UP TAB ---
            with tab2:
                st.write("") # Subtle spacing
                new_email = st.text_input("Work Email", key="signup_email", placeholder="attorney@lawfirm.com")
                new_password = st.text_input("Create Password", type="password", key="signup_pass", placeholder="Minimum 8 characters")
                
                if st.button("Start 1500-Page Trial"):
                    if not new_email or not new_password:
                        st.error("Please fill in all fields.")
                    else:
                        with st.spinner("Provisioning secure workspace..."):
                            try:
                                response = supabase.auth.sign_up({"email": new_email, "password": new_password})
                                
                                if response.user:
                                    user_id = response.user.id
                                    try:
                                        supabase.table("profiles").insert({
                                            "id": user_id,
                                            "email": new_email,
                                            "remaining_quota": 1500
                                        }).execute()
                                    except Exception:
                                        pass 
                                    
                                    st.success("Account created! You may now log in.")
                                else:
                                    st.info("Check your email for a secure confirmation link.")
                                    
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