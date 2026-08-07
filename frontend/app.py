import streamlit as st
import requests
import time
from datetime import datetime
import login_page
import fitz
import base64


BACKEND_URL = "https://green-box-intel.onrender.com"

def show_dashboard():

    


    st.markdown("""
    <style>
    /* ---------- GLOBAL ---------- */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #111827; /* Deep Slate (Main Text) */
    }

    .stApp {
        background-color: #FAFAFA; /* Off-White (Background) */
    }

    /* Paragraph text */
    p, .stMarkdown p {
        color: #4B5563 !important; /* Medium Gray */
    }

    /* Remove default top padding */
    .block-container {
        max-width: 98% !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 3.5rem !important;
        padding-bottom: 1rem !important;
    }

    /* ---------- HEADER BAR ---------- */
    header[data-testid="stHeader"] {
        background-color: #FAFAFA;
        border-bottom: 1px solid #e5e7eb;
        height: 3rem !important;
        z-index: 100;
    }

    header[data-testid="stHeader"]::after {
        content: "Green Box Intel"; /* Removed old emoji to match new brand */
        font-weight: 700;
        font-size: 1.1rem;
        color: #111827; /* Deep Slate */
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
    }

    /* ---------- CARDS (3 Columns) ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] > div > div {
        background-color: #ffffff; /* Pure white to pop against Off-White background */
        border-radius: 12px;
        border: 1px solid #e5e7eb; 
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.02);
    }

    /* ---------- HEADINGS ---------- */
    h1, h2, h3, h4, h5, h6 {
        color: #111827 !important; /* Deep Slate */
        font-weight: 700;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }

    /* ---------- BUTTONS (Modern Pill Design) ---------- */
    .stButton > button {
        background-color: #111827 !important; /* Deep Slate */
        color: #ffffff !important;
        border: 1px solid #111827 !important;
        border-radius: 999px !important;
        font-weight: 600;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* Fix for internal paragraph text to ensure it is white */
    .stButton > button p {
        color: #ffffff !important;
        margin: 0 !important;
    }

    .stButton > button:hover {
        background-color: #374151 !important; /* Lighter Slate on hover */
        border-color: #374151 !important;
        box-shadow: 0 4px 12px rgba(17, 24, 39, 0.2) !important;
        transform: translateY(-1px);
    }

    .stButton > button:hover p {
        color: #ffffff !important;
    }

    div[data-testid="column"] .stButton > button {
        width: 100%;
    }

    /* ---------- INPUTS & UPLOADER ---------- */
    /* Text Input Styling */
    .stTextInput input {
        border-radius: 8px;
        border: 1px solid #9CA3AF; /* Faded Gray */
        padding: 10px;
        color: #111827; /* Deep Slate */
    }

    /* Uploader Styling */
    div[data-testid="stFileUploader"] {
        border: 2px dashed #9CA3AF; /* Faded Gray */
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
    }
    div[data-testid="stFileUploader"]:hover {
        border-color: #111827; /* Deep Slate on hover */
        background-color: #FAFAFA;
    }
    div[data-testid="stFileUploader"] button {
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #9CA3AF !important;
        border-radius: 999px !important;
        padding: 4px 12px !important;
        font-weight: 600;
        margin-top: 5px;
    }

    /* ---------- FILE CARDS ---------- */
    .file-card {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 10px 14px;
        margin-top: 8px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .file-card-text {
        font-size: 0.85rem;
        color: #111827; /* Deep Slate */
        font-weight: 600;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 200px;
    }
    .file-card-sub {
        font-size: 0.75rem;
        color: #9CA3AF; /* Faded Gray */
    }

    /* ---------- CHAT BOX ---------- */
    .stChatMessage {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 10px;
        color: #4B5563; /* Medium Gray for easy reading */
    }

    /* ---------- SIDEBAR (Light Theme Update) ---------- */
    /* Changed from dark blue to Off-White to match dashboard UI screenshot */
    section[data-testid="stSidebar"] {
        background-color: #FAFAFA !important;
        border-right: 1px solid #e5e7eb;
        width: 260px !important;
    }

    /* Sidebar General Text - Deep Slate */
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] .stHeading,
    section[data-testid="stSidebar"] label {
        color: #111827 !important;
    }

    /* Forces the Collapse Arrow to be Deep Slate */
    [data-testid="stSidebarCollapseButton"] {
        color: #111827 !important;
    }
    [data-testid="stSidebarCollapseButton"] svg {
        fill: #111827 !important;
        stroke: #111827 !important;
    }

    /* Fix Dropdown & Input Text Colors */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
    section[data-testid="stSidebar"] div[data-baseweb="base-input"] input {
        color: #111827 !important; /* Deep Slate */
        -webkit-text-fill-color: #111827 !important;
        caret-color: #111827 !important;
        background-color: #ffffff !important;
        border: 1px solid #9CA3AF !important; /* Faded Gray */
    }

    
    </style>
    """, unsafe_allow_html=True)

    user_id = st.session_state.get("user_id")
    
    if not user_id:
        st.error("Session error. Please log in again.")
        return
        
    if 'viewing_history' not in st.session_state: st.session_state['viewing_history'] = False
    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    if "history_data" not in st.session_state: st.session_state.history_data = {}
    if 'history_list' not in st.session_state: st.session_state['history_list'] = {}

    if "pending_job_selection" in st.session_state:
        st.session_state["case_selector"] = st.session_state["pending_job_selection"]
        del st.session_state["pending_job_selection"]


    def load_history():
        """Fetches the list of past cases for the specific user from the Backend."""
        try:
            res = requests.get(f"{BACKEND_URL}/history", params={"user_id": user_id})
            
            if res.status_code == 200:
                st.session_state['history_list'] = res.json()
                
                # Optional: Calculate total active pages for this specific user
                total_active_pages = sum(job.get('pages', 0) for job in st.session_state['history_list'].values())
                st.session_state['total_system_pages'] = total_active_pages
            else:
                print(f"⚠️ Error {res.status_code}: {res.text}")
        except Exception as e:
            print(f"⚠️ Could not load history: {e}")

    if not st.session_state['history_list']:
        load_history()

    def reset_to_new_case():
        st.session_state["case_selector"] = "None"
        st.session_state['viewing_history'] = False
        st.session_state.chat_history = []

    def delete_case_callback(job_id):
        """
        Handles the API call with Authentication, State Reset, and Local Cache Cleanup.
        """
        try:
            user_id = st.session_state.get("user_id")
            
            res = requests.delete(
                f"{BACKEND_URL}/delete/{job_id}", 
                params={"user_id": user_id}
            )
            
            if res.status_code == 200:
                # 3. Reset Selection State
                st.session_state["case_selector"] = "None"
                st.session_state['viewing_history'] = False
                st.session_state.chat_history = []
                
                if 'history_list' in st.session_state:
                    if isinstance(st.session_state['history_list'], dict):
                        st.session_state['history_list'].pop(job_id, None)
                
                st.toast("✅ Case deleted successfully!")
            else:
                st.error(f"Failed to delete case: {res.text}")

        except Exception as e:
            st.error(f"Could not reach server: {e}")


    try:
        quota_res = requests.get(
            f"{BACKEND_URL}/quota", 
            params={"user_id": user_id} 
        )
        if quota_res.status_code == 200:
            quota_data = quota_res.json()
            used_pages = quota_data.get("used", 0)
            limit_pages = quota_data.get("limit", 1500)
        else:
            used_pages, limit_pages = 0, 1500
    except Exception as e:
        used_pages, limit_pages = 0, 1500
        st.sidebar.error("⚠️ Connection Error")

    
    past_jobs = {}
    try:
        history_res = requests.get(
            f"{BACKEND_URL}/history", 
            params={"user_id": user_id} 
        )
        if history_res.status_code == 200:
            past_jobs = history_res.json()
    except Exception:
        pass

    with open("frontend/assets/gbi3_logo.png", "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    st.sidebar.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0px;">
            <img src="data:image/png;base64,{img_b64}" width="40" style="mix-blend-mode: multiply; transform: translateY(-2px);">
            <h2 style="margin: 0; font-size: 1.5rem; color: #111827;">Green Box Intel</h2>
        </div>
    """, unsafe_allow_html=True)
    st.sidebar.caption("SECURE INTELLIGENCE")

    real_percent = used_pages / limit_pages
    visual_percent = min(max(real_percent, 0.05) if used_pages > 0 else 0.0, 1.0)

    st.sidebar.progress(visual_percent)
    st.sidebar.caption(f"{used_pages} / {limit_pages} Pages Used")
    st.sidebar.divider()

    if st.sidebar.button("🗂️ View Case Dashboard", use_container_width=True):
        st.session_state['show_dashboard'] = True
        st.session_state['viewing_history'] = False
        st.session_state["case_selector"] = "None" 
        st.rerun()

    job_list = list(past_jobs.keys()) if past_jobs else []
    
    job_list.sort(key=lambda x: past_jobs[x].get('metadata', {}).get('timestamp', ''), reverse=True)

    options_list = ["NEW_CASE_ID"] + job_list

    def format_job_label(job_id):
        if job_id == "NEW_CASE_ID":
            return "➕ New Case Analysis"
        
        job = past_jobs.get(job_id, {})
        case_name = job.get('case_name')
        if case_name and case_name != "None":
            return f"📂 {case_name[:22]}"
        
        
        fname = job.get('filename', job_id[:8])
        return f"📄 {fname[:22]}..."

    def on_case_change():
        """Wipes chat and temporary states when switching between cases."""
        st.session_state.chat_history = []
        for key in list(st.session_state.keys()):
            if key.startswith("edit_mode_") or key.startswith("in_"):
                del st.session_state[key]

    selected_job_id = st.sidebar.selectbox(
        "Your Cases",
        options=options_list,
        format_func=format_job_label,
        key="case_selector",
        index=None, 
        placeholder="Type to Search...",
        on_change=on_case_change
    )

    if selected_job_id == "NEW_CASE_ID" or selected_job_id is None:
        # Handle New Case or Cleared Search
        if selected_job_id == "NEW_CASE_ID":
            st.session_state['viewing_history'] = False
            st.session_state['show_dashboard'] = False
            
    elif selected_job_id in past_jobs:
        st.session_state['viewing_history'] = True
        st.session_state['show_dashboard'] = False
        
        st.session_state['history_data'] = past_jobs[selected_job_id]

    if st.session_state.get('show_dashboard', False):
        st.title("🗂️ Case Dashboard")
        st.caption(f"Account: {st.session_state['user'].email} | Total Active Cases: {len(past_jobs)}")
        st.divider()

        h1, h2, h3, h4, h5 = st.columns([0.35, 0.25, 0.15, 0.1, 0.15])
        h1.markdown("**Case Name**")
        h2.markdown("**File Name**")
        h3.markdown("**Date**")
        h4.markdown("**Pages**")
        h5.markdown("**Action**")
        st.divider()

        if not past_jobs:
            st.info("No cases found. Start a new analysis in the sidebar!")
        
        for j_id, j_data in past_jobs.items():
            with st.container():
                c1, c2, c3, c4, c5 = st.columns([0.35, 0.25, 0.15, 0.1, 0.15])
                
                name = j_data.get('case_name')
                if not name or str(name).strip().lower() == "none": 
                    name = "Unnamed Case"
                c1.write(f"📂 **{name}**")
                
                docs = j_data.get('documents', [])
                meta = j_data.get('metadata', {})
                
                if docs:
                    first_fname = docs[0].get('file_name', 'Unnamed File')
                    extra_files = len(docs) - 1
                    if extra_files > 0:
                        c2.write(f"📄 {first_fname[:15]}... (+{extra_files})")
                    else:
                        c2.write(f"📄 {first_fname[:20]}...")
                else:
                    file_list = meta.get('file_list', [])
                    if file_list:
                        c2.write(f"📄 {file_list[0][:15]}...")
                    else:
                        c2.write("📄 No files")
                
                raw_date = j_data.get('created_at') or meta.get('timestamp')
                date_str = str(raw_date)[:10] if raw_date else "Unknown"
                c3.write(date_str)
                
                pgs = j_data.get('total_pages', 0)
                c4.write(f"{pgs} pgs")
                
                def open_case(target_id=j_id):
                    st.session_state["case_selector"] = target_id
                    st.session_state['viewing_history'] = True
                    st.session_state['show_dashboard'] = False
                    st.session_state['history_data'] = past_jobs[target_id]
                
                c5.button("Open ↗️", key=f"open_{j_id}", on_click=open_case)
                
            st.divider() 
        st.stop()

    # 5. MAIN LAYOUT
    col1, col2, col3 = st.columns([1.1, 2.1, 0.8], gap="small")

    # ==========================================
    # COLUMN 1: INPUT & CONTROLS
    # ==========================================
    with col1:
        with st.container(border=True):
            st.subheader("📁 Case Input")
            
            if st.session_state['viewing_history']:
                temp_job_id = st.session_state['history_data'].get('job_id')
                
                if temp_job_id:
                    try:
                        check_res = requests.get(
                            f"{BACKEND_URL}/status/{temp_job_id}",
                            params={"user_id": user_id} 
                        )
                        if check_res.status_code == 200:
                            live_data = check_res.json()
                            
                            live_pages = live_data.get('pages', 0)
                            current_pages = st.session_state['history_data'].get('pages', 0)
                            live_status = live_data.get('status', '')
                            current_status = st.session_state['history_data'].get('status', '')

                            if (live_pages != current_pages) or (live_status != current_status and live_status == "Completed"):
                                st.session_state['history_data'] = live_data
                                st.rerun() 
                    except Exception:
                        pass

                # --- 2. HISTORY MODE UI ---
                data = st.session_state['history_data']
                h_col1, h_col2, h_col3 = st.columns([0.7, 0.2, 0.2])
                
                with h_col1:
                    edit_key = f"edit_mode_{selected_job_id}"
                    is_editing = st.session_state.get(edit_key, False)

                    c_name = data.get('case_name', 'Unnamed Case')
                    if not c_name or c_name == "None":
                        c_name = data.get('filename', 'Unknown File')

                    if is_editing:
                        # ✏️ RENAME INPUT
                        new_name_input = st.text_input("Rename", value=c_name, label_visibility="collapsed", key=f"in_{selected_job_id}")
                        
                        if st.button("💾 Save", key=f"save_{selected_job_id}"):
                            if new_name_input:
                                try:
                                    # --- AUTHENTICATED RENAME ---
                                    
                                    payload = {
                                        "new_name": new_name_input,
                                        "user_id": user_id
                                    }
                                    requests.put(f"{BACKEND_URL}/rename/{selected_job_id}", json=payload)
                                    
                                    
                                    data['case_name'] = new_name_input
                                    st.session_state[edit_key] = False 
                                    st.toast(f"✅ Renamed to: {new_name_input}")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Rename failed: {e}")
                    else:
                        
                        st.markdown(f"**{c_name}**")
                        st.caption(f"Processed: {data.get('timestamp', 'Unknown')[:10]}")

                # --- RENAME TOGGLE ---
                with h_col2:
                    if st.button("✏️", key=f"edit_btn_{selected_job_id}", help="Rename Case"):
                        st.session_state[edit_key] = not st.session_state.get(edit_key, False)
                        st.rerun()

                # --- DELETE BUTTON ---
                with h_col3:
                    
                    st.button(
                        "🗑️", 
                        type="primary", 
                        help="Delete this case",
                        key=f"del_btn_{selected_job_id}", 
                        on_click=delete_case_callback, 
                        args=(selected_job_id,)
                    )
                
                st.divider()
                st.markdown("**Files in this Case:**")

           
                documents = data.get('documents', [])

                if documents:
                    for doc in documents:
                        fname = doc.get('file_name', 'Unknown File')
                        p_count = doc.get('page_count', 0)
                        
                        st.markdown(
                            f"""
                            <div style="border: 1px solid #e6e9ef; border-radius: 5px; padding: 10px; margin-bottom: 10px; background-color: #fcfcfc;">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div style="display: flex; align-items: center; gap: 8px;">
                                        <span style="font-size: 1.2rem;">📄</span>
                                        <span style="font-weight: 500; font-size: 0.9rem;">{fname}</span>
                                    </div>
                                    <span style="font-size: 0.8rem; color: #6b7280; background: #f3f4f6; padding: 2px 8px; border-radius: 10px;">
                                        {p_count} pgs
                                    </span>
                                </div>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                else:
                    metadata = data.get('metadata', {})
                    raw_list = metadata.get('file_list', [])
                    
                    if not raw_list:
                        raw_list = [data.get('filename', '')]
                        
                    file_list = []
                    for item in raw_list:
                        if item:
                            # Split by comma, strip whitespace, and add to the clean list
                            file_list.extend([f.strip() for f in str(item).split(',')])
                            
                    
                    file_list = list(set([f for f in file_list if f]))

                    if file_list:
                        for fname in file_list:
                            st.markdown(
                                f"""
                                <div style="border-left: 3px solid #10b981; margin-bottom: 8px; padding-left: 10px; background: #f9f9f9; padding: 10px; border-radius: 4px;">
                                    <div style="display:flex; align-items:center; gap:10px;">
                                        <div style="color:#10b981; font-size: 1.2rem;">📄</div>
                                        <div style="font-weight: 500; font-size: 0.9rem;">{fname}</div>
                                    </div>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                    else:
                        st.info("No file records found.")

                if 'upload_key' not in st.session_state:
                    st.session_state['upload_key'] = 0
                
                with st.expander("➕ Append New PDF", expanded=False):
                    st.info("💡 Merges new info into the report without re-reading old files.")
                    new_files = st.file_uploader("Select PDF", type="pdf", accept_multiple_files=True, key=f"append_{st.session_state['upload_key']}")
                    
                    if new_files:
                        if st.button("Merge & Update", use_container_width=True):
                            with st.spinner("Integrating new records..."):
                                # Prepare Payload
                                files_payload = [
                                    ("files", (f.name, f.getvalue(), "application/pdf")) for f in new_files
                                ]
                                
                                try:
                                    res = requests.post(
                                        f"{BACKEND_URL}/append-files/{selected_job_id}", 
                                        files=files_payload,
                                        data={"user_id": user_id} # 
                                    )
                                    
                                    if res.status_code == 200:
                                        st.session_state['upload_key'] += 1
                                        st.success("Success! Reloading...")
                                        time.sleep(1)
                                        st.rerun()
                                    elif res.status_code == 403:
                                        st.error("🚫 Quota Exceeded for this update.")
                                    else:
                                        st.error("Failed to update.")
                                except Exception as e:
                                    st.error(f"Error: {e}")
                
                st.divider()
                st.button("← New Analysis", on_click=reset_to_new_case)
                    
            else:
                # --- UPLOAD MODE ---
                
                # 1. Case Name Input
                case_name_input = st.text_input("Case Name / Reference ID", placeholder="e.g. Smith v. Jones")
                
                st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True) # Spacer
                
                # 2. The Drop Zone
                uploaded_files = st.file_uploader(
                    "Upload Case Files", 
                    type="pdf", 
                    accept_multiple_files=True,
                    label_visibility="collapsed" 
                )
                
                if uploaded_files:
                    st.markdown("---")
                    
                    total_queue_pages = 0 
                    
                    for f in uploaded_files:
                        f_size = f.size / 1024 / 1024
                        
                       
                        try:
                            
                            doc = fitz.open(stream=f.read(), filetype="pdf")
                            page_count = len(doc)
                            total_queue_pages += page_count
                            
                            
                            f.seek(0) 
                        except Exception as e:
                            page_count = "Unknown"
                            f.seek(0)
                        
                       
                        st.markdown(
                            f"""
                            <div class="file-card" style="border: 1px solid #e5e7eb; border-radius: 8px; padding: 12px; margin-bottom: 8px; background: white;">
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <div style="display:flex; align-items:center; gap:10px;">
                                        <div style="background:#eff6ff; padding:8px; border-radius:6px; color:#3b82f6;">📄</div>
                                        <div>
                                            <div class="file-card-text" style="font-weight: 500; font-size: 0.95rem; color: #111827;">{f.name}</div>
                                            <div class="file-card-sub" style="font-size: 0.8rem; color: #6b7280;">
                                                {f_size:.1f} MB • {page_count} Pages • Ready
                                            </div>
                                        </div>
                                    </div>
                                    <div style="color:#10b981; font-size: 0.8rem;">●</div>
                                </div>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # --- NEW: Display the Total Quota Alert ---
                    st.info(f"📊 **Pre-Analysis Check:** {len(uploaded_files)} files ready | **{total_queue_pages} Total Pages** will be processed.")
                    
                    # Check if name is provided
                    if st.button("Start Intelligence Engine"):
                        if not case_name_input:
                            st.warning("⚠️ Please give this case a name before starting.")
                        else:
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            try:
                                files = [("files", (f.name, f.getvalue(), "application/pdf")) for f in uploaded_files]
                                
                                # --- Upload Phase (Sending case_name AND user_id) ---
                                status_text.caption("Phase 1: Encrypting & Uploading...")
                                with st.spinner("Processing..."):
                                    resp = requests.post(
                                        f"{BACKEND_URL}/process-intelligence", 
                                        files=files,
                                        data={
                                            "case_name": case_name_input,
                                            "user_id": user_id  # <--- CRITICAL UPDATE
                                        } 
                                    )
                                
                                if resp.status_code == 200:
                                    job_id = resp.json().get("job_id")
                                    status = "Starting"
                                    
                                    while status not in ["Completed", "Failed"]:
                                        time.sleep(1.5)
                                        
                                        res = requests.get(
                                            f"{BACKEND_URL}/status/{job_id}",
                                            params={"user_id": user_id} 
                                        ).json()
                                        
                                        status = res.get("status")
                                        if "Extracting" in status: 
                                            progress_bar.progress(40)
                                            status_text.caption("Phase 2: OCR Extraction...")
                                        elif "Generating" in status: 
                                            progress_bar.progress(80)
                                            status_text.caption("Phase 3: AI Analysis...")
                                    
                                    if status == "Completed":
                                        progress_bar.progress(100)
                                        st.session_state['viewing_history'] = True
                                        st.session_state['history_data'] = res
                                        st.session_state['chat_history'] = []
                                        st.session_state["pending_job_selection"] = job_id
                                        st.rerun()
                                elif resp.status_code == 403:
                                    st.error("🚫 Quota Exceeded: You do not have enough pages.")
                                else: 
                                    st.error(f"Server Error: {resp.status_code}")
                                    st.write(resp.text) 
                            except Exception as e: st.error(f"Error: {e}")

    # ==========================================
    # COLUMN 2: THE CHRONOLOGY
    # ==========================================
    with col2:
        with st.container(border=True):
            h1, h2 = st.columns([3, 1])
            with h1: st.subheader("Medical Chronology")
            with h2:
               
                dl_id = selected_job_id
                
                
                curr_data = st.session_state.get('history_data', {})

                
                if (dl_id == "None" or dl_id is None) and curr_data:
                   
                    for k, v in past_jobs.items():
                        if v.get('timestamp') == curr_data.get('timestamp'): 
                            dl_id = k
                            break
                    
                    if not dl_id or dl_id == "None":
                        dl_id = curr_data.get('job_id')
                
                
                if st.session_state['viewing_history'] and dl_id and dl_id != "None":
                    # --- AUTHENTICATED DOWNLOAD ---
                    try:
                        
                        response = requests.get(
                            f"{BACKEND_URL}/download-report/{dl_id}",
                            params={"user_id": user_id} 
                        )
                        
                        if response.status_code == 200:
                            
                            cd_header = response.headers.get('Content-Disposition')
                            fname = f"Medical_Chronology_{dl_id[:8]}.docx"
                            if cd_header and "filename=" in cd_header:
                                fname = cd_header.split("filename=")[1].strip('"')

                            st.download_button(
                                label="📥 Download",
                                data=response.content,
                                file_name=fname,
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                        else:
                            st.caption("⚠️ Report processing...")
                    except Exception as e:
                        st.error("Connection Error")

            # --- DISPLAY CONTENT ---
            if st.session_state['viewing_history']:
                data = st.session_state['history_data']
                
                
                m1, m2 = st.columns(2)

                
                metadata = data.get('metadata', {})

                
                billed_amount = metadata.get('total_damages', 0.0)

                
                if billed_amount is None: billed_amount = 0.0

                m1.metric("Total Damages", f"${billed_amount:,.2f}")
                m2.metric("Volume", f"{data.get('total_pages', 0)} Pages")
                
                st.divider()
                
                
                with st.container(height=600):
                    
                    text_content = data.get('chronology', '')
                    if not text_content:
                        text_content = data.get('chronology_text', '*Analysis in progress...*')
                    
                    st.markdown(text_content)
            else:
                
                st.markdown(
                    """
                    <div style="text-align: center; padding: 60px; color: #94a3b8;">
                        <h4>Waiting for Documents</h4>
                        <p>Upload a case file to generate the chronology.</p>
                    </div>
                    """, unsafe_allow_html=True
                )

    # ==========================================
    # COLUMN 3: AI ASSISTANT
    # ==========================================
    with col3:
        with st.container(border=True):
            st.subheader("💬 Assistant")
            st.caption("Ask questions about this specific case.")

            if st.session_state['viewing_history']:
                
                chat_container = st.container(height=450)
                
               
                with chat_container:
                    for msg in st.session_state.chat_history:
                        with st.chat_message(msg["role"]):
                            st.write(msg["content"])
                
                
                if prompt := st.chat_input("Ex: What are the injuries?"):
                    
                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                    with chat_container:
                        st.chat_message("user").write(prompt)
                    
                   
                    c_id = selected_job_id
                    if (c_id == "None" or c_id is None) and st.session_state.get('history_data'):
                        
                        hist_data = st.session_state['history_data']
                        c_id = hist_data.get('job_id')
                        
                        if not c_id:
                            for k, v in past_jobs.items():
                                if v.get('timestamp') == hist_data.get('timestamp'): 
                                    c_id = k; break
                    
                    
                    if c_id and c_id != "None":
                        with chat_container:
                            with st.spinner("Analyzing..."):
                                try:
                                    
                                    payload = {
                                        "query": prompt, 
                                        "user_id": user_id 
                                    }
                                    
                                    resp = requests.post(f"{BACKEND_URL}/chat/{c_id}", json=payload)
                                    
                                    if resp.status_code == 200:
                                        ans = resp.json().get("answer")
                                    else:
                                        ans = f"⚠️ Server Error: {resp.status_code}"
                                        
                                except Exception as e:
                                    ans = "⚠️ Connection Error. Please try again."
                            
                            
                            st.chat_message("assistant").write(ans)
                            st.session_state.chat_history.append({"role": "assistant", "content": ans})
            else:
                
                st.info("Chat unavailable until analysis is complete.")