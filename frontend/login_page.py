import streamlit as st
import os
import sys
import time
import uuid
import hashlib
import base64

# Add the parent directory to Python's path so it can find the backend folder
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

# Import the SQLAlchemy engine from your new AWS backend
from backend.database import engine
from sqlalchemy import text

def hash_password(password: str) -> str:
    """Securely hashes the password using SHA-256 before saving to AWS."""
    return hashlib.sha256(password.encode()).hexdigest()

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

            with open("frontend/assets/gbi3_logo.png", "rb") as f:
                logo_base64 = base64.b64encode(f.read()).decode()
            
            # --- CARD HEADER ---
            st.markdown(f"""
                <div class="centered-header">
                    <img src="data:image/png;base64,{logo_base64}" width="60" style="margin-bottom: 10px;">
                    <h2 style='padding-top: 0rem; margin-bottom: 0px; color: #111827;'>Green Box Intel</h2>
                    <p style='color: #6B7280; font-size: 0.9rem; margin-top: 5px;'>Secure Medical Chronologies</p>
                </div>
            """, unsafe_allow_html=True)

            # --- TABS ---
            tab1, tab2 = st.tabs(["Sign In", "Request Access"])
    
    # --- LOGIN TAB ---
    with tab1:
        st.write("") 
        email = st.text_input("Email Address", key="login_email", placeholder="attorney@lawfirm.com")
        password = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
        
        if st.button("Sign In"):
            if not email or not password:
                st.error("Please enter both email and password.")
            else:
                with st.spinner("Authenticating..."):
                    try:
                        # 1. Query AWS RDS for the user's profile
                        query = text("SELECT id, email, password_hash FROM profiles WHERE email = :email")
                        with engine.connect() as conn:
                            result = conn.execute(query, {"email": email}).mappings().first()
                            
                        # 2. Verify the hashed password matches
                        if result and result["password_hash"] == hash_password(password):
                            # 3. Create the secure local session
                            st.session_state["user_id"] = result["id"]
                            st.session_state["user_email"] = result["email"]
                            st.session_state["page"] = "dashboard"
                            
                            st.success("Access granted. Redirecting...")
                            time.sleep(1)
                            st.query_params.clear()
                            st.rerun()
                        else:
                            st.error("Invalid email or password.")
                    except Exception as e:
                        st.error(f"Authentication service unavailable: {str(e)}")

    # --- SIGN UP (REQUEST ACCESS) TAB ---
    with tab2:
        st.write("") 
        new_email = st.text_input("Work Email", key="signup_email", placeholder="attorney@lawfirm.com")
        new_password = st.text_input("Create Password", type="password", key="signup_pass", placeholder="Minimum 8 characters")
        
        if st.button("Request Access"):
            if not new_email or not new_password:
                st.error("Please fill in all fields.")
            elif any(domain in new_email for domain in [ "@yahoo", "@outlook"]):
                st.warning("Please use your professional law firm email address.")
            else:
                with st.spinner("Submitting request..."):
                    try:
                        # 1. Generate secure credentials
                        new_user_id = str(uuid.uuid4())
                        hashed_pw = hash_password(new_password)
                        
                        # 2. Insert directly into AWS profiles table
                        insert_query = text("""
                            INSERT INTO profiles (id, email, password_hash, remaining_quota, is_approved) 
                            VALUES (:id, :email, :password_hash, 0, false)
                        """)
                        
                        with engine.begin() as conn:
                            conn.execute(insert_query, {
                                "id": new_user_id,
                                "email": new_email,
                                "password_hash": hashed_pw
                            })
                            
                        # 3. Success Feedback
                        st.success("✅ Request Submitted Successfully!")
                        st.info("""
                            **Next Steps:**
                            1. Check your email to verify your address.
                            2. Our team will verify your firm's credentials.
                            3. Once approved, your service will be activated automatically.
                        """)
                    except Exception as e:
                        # Catch duplicate emails (PostgreSQL Unique Violation)
                        if "duplicate key" in str(e).lower() or "uniqueviolation" in str(e).lower():
                            st.error("An account with this email already exists.")
                        else:
                            st.error(f"Sign up failed: {str(e)}")

def is_authenticated():
    """Returns True if user is logged in, False otherwise."""
    return "user_id" in st.session_state

def handle_logout():
    """Handles the 'Logout' button and clears the local session."""
    with st.sidebar:
        st.divider()
        user_email = st.session_state.get('user_email', 'Unknown User')
        st.caption(f"Logged in as: {user_email}")
        
        if st.button("Log Out"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()