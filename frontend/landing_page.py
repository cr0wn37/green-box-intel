import streamlit as st
import requests
import base64

def send_email(email, details):
    # This is the "Engine" that talks to Formspree
    FORMSPREE_URL = "https://formspree.io/f/xykdlvay"
    data = {
        "email": email, 
        "message": f"Quote Request: {details}"
    }
    response = requests.post(FORMSPREE_URL, json=data)
    return response.status_code == 200

def show_landing_page():

    # ==========================================
    # 1. STANDALONE GLASS NAVBAR COMPONENT
    # ==========================================
    image_path = "frontend/assets/gbi3_logo.png" 
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden !important;}
        [data-testid="stToolbar"] {visibility: hidden !important;}
        [data-testid="stDecoration"] {visibility: hidden !important;}
        [data-testid="stStatusWidget"] {visibility: hidden !important;}
        /* This hides the "made with streamlit" in the embedded iframe */
        .embeddedAppMetaInfoBar_container__DxxL1 {display: none !important;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        /* 1. Global Spacing */
        .block-container {
            padding-top: 6rem !important; 
        }
        
        header { visibility: hidden !important; }

        /* 2. THE NAVBAR PILL - BALANCED ROW */
        div[data-testid="stHorizontalBlock"]:has(.nav-brand-logo) {
            position: fixed !important;
            top: 20px !important;
            left: 0 !important;
            right: 0 !important;
            margin: auto !important;
            width: 90% !important;
            max-width: 1200px !important;
            z-index: 999999 !important;
            
            background: rgba(255, 255, 255, 0.25) !important;
            backdrop-filter: blur(16px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(16px) saturate(180%) !important;
            
            border: 1px solid rgba(0, 0, 0, 0.08) !important;
            border-radius: 50px !important;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.15) !important;
            
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important; 
            padding: 8px 35px !important;
            min-height: 60px !important;
        }

        /* 🔴 THE FIX: Strip invisible bottom margins from Streamlit's <p> wrappers! */
        div[data-testid="stHorizontalBlock"]:has(.nav-brand-logo) p {
            margin: 0 !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
        }

        /* 3. LOGO ALIGNMENT */
        div[data-testid="stHorizontalBlock"]:has(.nav-brand-logo) div[data-testid="column"]:first-child {
            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;
            height: 100% !important;
            min-height: 44px !important; 
        }

        .nav-brand-logo {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.25rem;
            font-weight: 800;
            color: #111827;
            display: flex !important;
            align-items: center !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: normal !important; 
            white-space: nowrap;
            
            /* 🔴 THE MANUAL NUDGE FIX: Pulls the logo up. Change the -4px to -2px or -6px to dial it in perfectly. */
            transform: translateY(-8px) !important; 
        }

        /* 4. ABSOLUTE CENTERED LINKS */
        .nav-menu-links {
            display: flex !important;
            position: absolute !important;
            left: 50% !important;
            top: 50% !important;
            transform: translate(-50%, -50%) !important;
            gap: 32px;
            margin: 0 !important;
            white-space: nowrap;
            z-index: 10;
        }

        .nav-menu-links a {
            font-family: 'Plus Jakarta Sans', sans-serif;
            text-decoration: none;
            color: #4B5563;
            font-weight: 600;
            font-size: 0.95rem;
            transition: color 0.2s ease;
        }

        .nav-menu-links a:hover {
            color: #000000;
        }

        /* 5. BUTTON ALIGNMENT (FAR RIGHT) */
        div[data-testid="stHorizontalBlock"]:has(.nav-brand-logo) div[data-testid="column"]:last-child {
            display: flex !important;
            justify-content: flex-end !important;
            align-items: center !important;
            height: 100% !important;
            min-height: 44px !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.nav-brand-logo) div[data-testid="stElementContainer"] {
            margin-bottom: 0 !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.nav-brand-logo) .stButton button {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border-radius: 50px !important;
            padding: 0.5rem 1.6rem !important;
            font-size: 0.9rem !important;
            font-weight: 600 !important;
            margin: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- NAVBAR LAYOUT ---
    nav_col1, nav_col2, nav_col3 = st.columns([1.5, 2, 1], vertical_alignment="center")

    with nav_col1:
    # Flexbox locks the image and text side-by-side perfectly vertically centered
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 10px;">
                <img src="data:image/png;base64,{img_b64}" width="55" style="mix-blend-mode: multiply;transform: translateY(-8px);">
                <div class="nav-brand-logo" style="margin: 0; padding: 0; font-weight: bold; font-size: 1.3rem;">Green Box Intel</div>
            </div>
        """, unsafe_allow_html=True)
        
    with nav_col2:
        st.markdown("""
            <div class="nav-menu-links">
                <a href="#how-it-works">How it Works</a>
                <a href="#benefits">Benefits</a>
                <a href="#pricing">Pricing</a>
            </div>
        """, unsafe_allow_html=True)
        
    with nav_col3:
        if st.button("Client Login", key="nav_login_btn"):
            st.session_state.page = "login"
            st.rerun()
            
    # ==========================================
    # (Your Hero Section and Global CSS start below this)
    # ==========================================
    # 1. Advanced Custom CSS Injection
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        /* 🔴 FIX 1: Use .stApp instead of [class*="css"] so the glass isn't blocked by solid gray! */
        html, body, .stApp {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            background-color: #FAFAFA !important;
        }
        
        /* 🔴 FIX 2: Add 140px of top padding so the fixed navbar doesn't cover your Hero text */
        .block-container {
            padding-top: 10px !important; 
            padding-bottom: 0rem !important;
            max-width: 1300px !important;
        }
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        

        /* --- 2. HERO SECTION STYLES --- */
        .hero-left-align { 
            padding-right: 140px; /* Increased from 80px to create a large physical gap */
            text-align: left; 
            margin-top: 100px; 
        }
        .hero-title { font-size: 4.5rem; font-weight: 800; color: #111827; line-height: 1.05; letter-spacing: -0.04em; margin-bottom: 1.5rem; }
        .hero-title span { color: #9CA3AF; }
        .hero-subtitle { font-size: 1.25rem; font-weight: 500; color: #4B5563; max-width: 600px; line-height: 1.5; }
        .hero-right-align { 
            display: flex; 
            justify-content: flex-end; 
            width: 100%; 
            margin-top: 100px; /* This pushes the animation box down */
        }
        .hero-visual-card-large { background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%); border: 1px solid #E5E7EB; border-radius: 32px; height: 440px; width: 100%; min-width: 480px; position: relative; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.04); display: flex; align-items: center; justify-content: center; }

        

        /* --- THE "MESSY TO GOLDEN" PIPELINE ANIMATION --- */
        .g-pipeline {
            position: relative;
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            perspective: 1000px;
        }

        /* 1. The Messy Input Pages */
        .g-in-doc {
            position: absolute;
            width: 45px;
            height: 65px;
            background: #FFFFFF;
            border-radius: 6px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 10px 20px rgba(0,0,0,0.08);
            z-index: 5;
            opacity: 0;
        }
        /* Tiny gray lines inside to match your screenshot's text layout */
        .g-in-doc::before {
            content: ''; position: absolute; top: 10px; left: 8px; width: 65%; height: 3px; background: #CBD5E1; border-radius: 2px;
            box-shadow: 0 8px 0 #CBD5E1, 0 16px 0 #CBD5E1, 0 24px 0 #CBD5E1, 0 32px 0 #CBD5E1;
        }

        /* Slower 8-second staggered flying animations */
        .g-in-1 { animation: fly-in-1 8s infinite cubic-bezier(0.25, 0.8, 0.25, 1); }
        .g-in-2 { animation: fly-in-2 8s infinite cubic-bezier(0.25, 0.8, 0.25, 1); animation-delay: 0.3s; }
        .g-in-3 { animation: fly-in-3 8s infinite cubic-bezier(0.25, 0.8, 0.25, 1); animation-delay: 0.6s; }

        /* The new keyframes give them a lot more time to travel and pause before entering */
        @keyframes fly-in-1 {
            0% { transform: translate(-180px, -40px) rotate(-20deg) scale(1.1); opacity: 0; }
            5% { opacity: 1; }
            25% { transform: translate(-30px, -10px) rotate(-5deg) scale(0.5); opacity: 1; } /* Lingers near the slot */
            35% { transform: translate(0, 0) rotate(0deg) scale(0.1); opacity: 0; } /* Sucked in */
            100% { opacity: 0; }
        }
        @keyframes fly-in-2 {
            0% { transform: translate(-190px, 20px) rotate(15deg) scale(1.1); opacity: 0; }
            5% { opacity: 1; }
            25% { transform: translate(-30px, 0px) rotate(5deg) scale(0.5); opacity: 1; } 
            35% { transform: translate(0, 0) rotate(0deg) scale(0.1); opacity: 0; }
            100% { opacity: 0; }
        }
        @keyframes fly-in-3 {
            0% { transform: translate(-160px, 80px) rotate(-10deg) scale(1.1); opacity: 0; }
            5% { opacity: 1; }
            25% { transform: translate(-30px, 10px) rotate(-2deg) scale(0.5); opacity: 1; } 
            35% { transform: translate(0, 0) rotate(0deg) scale(0.1); opacity: 0; }
            100% { opacity: 0; }
        }

        /* 2. The New AI Engine (Rounded Monolith from Screenshot) */
        .g-machine {
            position: relative;
            width: 90px;
            height: 120px;
            background: #0A0A0A; /* Pure sleek black */
            border-radius: 24px; /* Much softer rounded corners */
            z-index: 10;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
            animation: box-process 8s infinite;
        }
        /* The vertical blue laser slot */
        .g-machine-slot {
            width: 6px;
            height: 45px;
            background: #111827;
            border-radius: 4px;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.5); /* Looks indented when off */
            animation: slot-glow 8s infinite;
        }

        /* Box pulses at exactly 35% when the last page goes in */
        @keyframes box-process {
            0%, 32% { box-shadow: 0 15px 35px rgba(0,0,0,0.15); transform: scale(1); }
            38%, 45% { box-shadow: 0 0 50px rgba(37, 99, 235, 0.2); transform: scale(1.05); } 
            52%, 100% { box-shadow: 0 15px 35px rgba(0,0,0,0.15); transform: scale(1); }
        }
        @keyframes slot-glow {
            0%, 32% { background: #111827; box-shadow: inset 0 2px 4px rgba(0,0,0,0.5); }
            38%, 45% { background: #3B82F6; box-shadow: 0 0 15px #3B82F6, 0 0 30px #3B82F6; } /* Ignites blue */
            52%, 100% { background: #111827; box-shadow: inset 0 2px 4px rgba(0,0,0,0.5); }
        }

        /* 3. The Golden Output Page (Timings adjusted for 8s loop) */
        .g-out-doc {
            position: absolute;
            width: 65px;
            height: 90px;
            background: linear-gradient(135deg, #FDE68A 0%, #F59E0B 100%);
            border-radius: 6px;
            z-index: 5;
            opacity: 0;
            overflow: hidden;
            animation: fly-out 8s infinite cubic-bezier(0.2, 0.8, 0.2, 1);
        }
        .g-out-doc::before {
            content: ''; position: absolute; top: 16px; left: 10px; width: 70%; height: 4px; background: rgba(255,255,255,0.9); border-radius: 2px;
            box-shadow: 0 12px 0 rgba(255,255,255,0.8), 0 24px 0 rgba(255,255,255,0.6), 0 36px 0 rgba(255,255,255,0.4);
        }
        .g-out-doc::after {
            content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
            background: linear-gradient(to right, transparent, rgba(255,255,255,0.6), transparent);
            animation: shimmer 8s infinite;
        }

        @keyframes fly-out {
            0%, 45% { transform: translate(0, 0) scale(0.2); opacity: 0; box-shadow: 0 0 0 transparent; }
            50% { opacity: 1; }
            75% { transform: translate(150px, 0) scale(1.3); opacity: 1; box-shadow: 0 20px 40px rgba(245, 158, 11, 0.4); } 
            90%, 100% { transform: translate(180px, 0) scale(1); opacity: 0; }
        }
        @keyframes shimmer {
            0%, 60% { left: -100%; }
            80%, 100% { left: 200%; }
        }

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

        /* Active/Click state fix */
        div.stButton > button:active {
            background-color: #000000 !important;
            border-color: #000000 !important;
            transform: translateY(0);
        }

        /* --- 3. CONTACT & FOOTER STYLES --- */
        .contact-section {
            padding: 100px 0;
            background-color: #FAFAFA;
        }

        .footer-container {
            background-color: #0A0A0A; /* Deep black/charcoal */
            color: #9CA3AF;
            padding: 80px 40px 40px 40px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            border-top: 1px solid #1F2937;
        }

        .footer-logo {
            color: #FFFFFF;
            font-size: 1.5rem;
            font-weight: 800;
            margin-bottom: 20px;
        }

        .footer-link {
            color: #9CA3AF;
            text-decoration: none;
            transition: color 0.2s ease;
            display: block;
            margin-bottom: 12px;
            font-weight: 500;
        }

        .footer-link:hover {
            color: #FFFFFF;
        }

        .footer-bottom {
            margin-top: 60px;
            padding-top: 20px;
            border-top: 1px solid #1F2937;
            font-size: 0.85rem;
            display: flex;
            justify-content: space-between;
        }
        </style>
    """, unsafe_allow_html=True)

    # 3. Hero Section Layout (CSS is handled globally now)
    col1, col2 = st.columns([1.4, 1], gap="large") # Increased to 1.4
    
    with col1:
        st.markdown("""
            <div class="hero-left-align">
                <div class="hero-title">
                    Cut the discovery time. <br><span>Build the winning chronology.</span>
                </div>
                <div class="hero-subtitle">
                    Stop wasting hours on manual document review. Our Intelligence Engine transforms thousands of medical pages into structured insights in minutes.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="hero-right-align">
                <div class="hero-visual-card-large">
                    <div class="g-pipeline">
                        <div class="g-in-doc g-in-1"></div>
                        <div class="g-in-doc g-in-2"></div>
                        <div class="g-in-doc g-in-3"></div>
                        <div class="g-machine">
                            <div class="g-machine-slot"></div>
                        </div>
                        <div class="g-out-doc"></div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # --- INTERACTIVE BENEFITS SECTION ---
    st.markdown("""
<style>
.benefits-wrapper {
    margin-top: 120px;
    margin-bottom: 120px;
    text-align: center;
}

.section-title {
    font-size: 3rem;
    font-weight: 800;
    color: #111827;
    letter-spacing: -0.03em;
    margin-bottom: 16px;
    line-height: 1.1;
}

.benefits-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px; /* Slightly tighter gap for cards */
    margin-top: 70px;
    text-align: left;
}

/* --- THE INTERACTIVE CARD --- */
.benefit-card {
    background: #FFFFFF;
    padding: 36px;
    border-radius: 24px;
    border: 1px solid rgba(229, 231, 235, 0.5); /* Very subtle border */
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); /* Smooth premium ease */
    position: relative;
    top: 0;
}

/* Hover State: Lift and Shadow */
.benefit-card:hover {
    box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.1); /* Soft, deep shadow */
    transform: translateY(-6px); /* Gentle lift */
    border-color: transparent;
}

/* --- THE ICON BOX --- */
.benefit-icon-box {
    width: 64px;
    height: 64px;
    background: #F3F4F6; /* Light gray default state */
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    margin-bottom: 24px;
    transition: all 0.3s ease;
    color: #111827;
}

/* Hover State: Icon turns dark for contrast */
.benefit-card:hover .benefit-icon-box {
    background: #111827;
    color: #FFFFFF;
}

.benefit-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 12px;
    letter-spacing: -0.02em;
}

.benefit-desc {
    font-size: 1rem;
    color: #6B7280;
    line-height: 1.6;
}
</style>

<div class="benefits-wrapper">
    <div class="section-title">Legal intelligence, <br>measured in results.</div>
    <p class="section-subtitle" style="max-width: 600px; margin: 0 auto;">Move beyond manual review with an AI pipeline designed specifically for high-stakes injury litigation.</p>
    <div class="benefits-grid">
        <div class="benefit-card">
            <div class="benefit-icon-box">⏱️</div>
            <div class="benefit-title">Save 20+ Hours Per Week</div>
            <div class="benefit-desc">Automate the manual sorting and summarizing of medical records. Turn days of paralegal work into minutes of AI processing.</div>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon-box">🎯</div>
            <div class="benefit-title">100% Citation Accuracy</div>
            <div class="benefit-desc">Every extracted medical event is linked directly to its exact source page and line number for ironclad court-readiness.</div>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon-box">🧠</div>
            <div class="benefit-title">Instant Case Insights</div>
            <div class="benefit-desc">Don't just read reports; chat with your case files to find hidden 'smoking gun' evidence or pre-existing conditions in seconds.</div>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon-box">🛡️</div>
            <div class="benefit-title">Automated Privacy Shield</div>
            <div class="benefit-desc">Instantly redact sensitive PII across thousands of pages to ensure HIPAA compliance without manual review cycles.</div>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon-box">📂</div>
            <div class="benefit-title">Unified Case Organization</div>
            <div class="benefit-desc">Consolidate disparate PDFs into a single, structured digital dashboard for clear visibility across your entire caseload.</div>
        </div>
        <div class="benefit-card">
            <div class="benefit-icon-box">📈</div>
            <div class="benefit-title">Bespoke Scalability</div>
            <div class="benefit-desc">Architected to handle any volume seamlessly, from boutique practice individual cases to national firm portfolios.</div>
        </div>
    </div>
</div>
    """, unsafe_allow_html=True)

    # 4. "How It Works" Section
    # 4. "How It Works" Section (Upgraded Visual Layout)
    st.markdown("""
        <style>
        /* Upgraded Section Title */
        .section-header {
            text-align: center;
            margin-top: 120px;
            margin-bottom: 80px;
        }
        .section-title {
            font-size: 3rem;
            font-weight: 800;
            color: #111827;
            letter-spacing: -0.04em;
            margin-bottom: 16px;
        }
        .section-subtitle {
            font-size: 1.2rem;
            color: #6B7280;
            max-width: 600px;
            margin: 0 auto;
        }

        /* Alternating Row Layout */
        .hiw-container {
            display: flex;
            flex-direction: column;
            gap: 100px;
            padding: 0 20px;
        }
        .hiw-row {
            display: flex;
            align-items: center;
            gap: 80px;
        }
        .hiw-row.reverse {
            flex-direction: row-reverse;
        }
        
        /* Text Side */
        .hiw-text {
            flex: 1;
        }
        .hiw-step-badge {
            display: inline-block;
            background: #EFF6FF;
            color: #2563EB;
            font-size: 0.85rem;
            font-weight: 700;
            padding: 6px 12px;
            border-radius: 999px;
            margin-bottom: 16px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }
        .hiw-text h3 {
            font-size: 2.2rem;
            font-weight: 800;
            color: #0B132B;
            margin-bottom: 16px;
            line-height: 1.2;
            letter-spacing: -0.02em;
        }
        .hiw-text p {
            font-size: 1.1rem;
            color: #4B5563;
            line-height: 1.6;
            margin-bottom: 24px;
        }

        /* Visual Side (The Image/Video Container) */
        .hiw-visual {
            flex: 1;
            background: linear-gradient(135deg, #F8FAFC 0%, #E2E8F0 100%);
            border: 1px solid #E5E7EB;
            border-radius: 24px;
            height: 400px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.04);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Minimalist Custom Bullets */
        .hiw-bullets {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .hiw-bullets li {
            display: flex;
            align-items: center;
            gap: 12px;
            color: #374151;
            font-weight: 500;
            margin-bottom: 14px;
            font-size: 1rem;
        }

        /* Creating the Bespoke Black Dot */
        .hiw-bullets li::before {
            content: "";
            width: 6px;
            height: 6px;
            background-color: #000000; /* Matching your new button color */
            border-radius: 50%;
            display: inline-block;
            flex-shrink: 0; /* Prevents the dot from squishing */
        }

        /* --- PURE CSS ILLUSTRATIONS (Placeholders for your GIFs) --- */
        
        /* Graphic 1: Upload Box */
        .g-upload {
            width: 60%; height: 60%; background: white; border: 2px dashed #94A3B8; border-radius: 16px;
            display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05); transition: transform 0.3s;
        }
        .hiw-visual:hover .g-upload { transform: scale(1.05); border-color: #2563EB; }
        
        /* Graphic 2: AI Scanner */
        .g-doc {
            width: 50%; height: 70%; background: white; border-radius: 12px; padding: 24px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.08); position: relative; overflow: hidden;
        }
        .g-line { height: 8px; background: #E2E8F0; margin-bottom: 16px; border-radius: 4px; }
        .g-line.redacted { background: #111827; width: 60%; display: inline-block; }
        .g-scanner {
            position: absolute; left: 0; right: 0; height: 3px; background: #2563EB;
            box-shadow: 0 0 20px 4px rgba(37,99,235,0.4); animation: scan 2.5s infinite alternate ease-in-out;
        }
        @keyframes scan { 0% { top: 10%; } 100% { top: 90%; } }

        /* Graphic 3: Dashboard Mock */
        .g-dash { display: flex; gap: 16px; width: 80%; height: 60%; }
        .g-table { flex: 2; background: white; border-radius: 12px; padding: 16px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); }
        .g-chat { flex: 1; background: #111827; border-radius: 12px; padding: 16px; display: flex; flex-direction: column; gap: 12px; }
        .g-t-row { height: 12px; background: #F1F5F9; margin-bottom: 10px; border-radius: 4px; }
        .g-c-bub { height: 16px; background: #334155; border-radius: 8px; width: 80%; }
        .g-c-bub.right { background: #2563EB; align-self: flex-end; width: 60%; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
<div id="how-it-works" class="section-header">
    <div class="section-title">From messy records to clear answers.</div>
    <div class="section-subtitle">See how our AI pipeline processes your case files in three simple steps.</div>
</div>

<div class="hiw-container">
    <div class="hiw-row">
        <div class="hiw-text">
            <div class="hiw-step-badge">Step 1</div>
            <h3>Upload the Case File</h3>
            <p>Stop sorting papers manually. Simply drag and drop hundreds of pages of disorganized medical records directly into your secure, encrypted dashboard.</p>
            <ul class="hiw-bullets">
                <li> Accepts up to 200MB per file</li>
                <li> End-to-end bank-grade encryption</li>
                <li> Append new files at any time</li>
            </ul>
        </div>
        <div class="hiw-visual">
            <div class="g-upload">
                <div style="font-size: 3rem;">📁</div>
                <div style="color: #64748B; font-weight: 500;">Drop PDFs here</div>
            </div>
        </div>
    </div>
    <div class="hiw-row reverse">
        <div class="hiw-text">
            <div class="hiw-step-badge">Step 2</div>
            <h3>AI Extraction & Redaction</h3>
            <p>Our custom legal AI instantly reads every page. It scrubs sensitive PII, calculates billing ledgers, and structures events into a precise chronological timeline.</p>
            <ul class="hiw-bullets">
                <li> Zero-retention AI models</li>
                <li> Automatic PII blackouts</li>
                <li> Accurate date and event mapping</li>
            </ul>
        </div>
        <div class="hiw-visual">
            <div class="g-doc">
                <div class="g-scanner"></div>
                <div class="g-line" style="width: 80%;"></div>
                <div class="g-line" style="width: 90%;"></div>
                <div class="g-line" style="width: 40%;"><div class="g-line redacted"></div></div>
                <div class="g-line" style="width: 85%;"></div>
                <div class="g-line" style="width: 70%;"></div>
            </div>
        </div>
    </div>
    <div class="hiw-row">
        <div class="hiw-text">
            <div class="hiw-step-badge">Step 3</div>
            <h3>Review & Contextual Chat</h3>
            <p>Export your finished chronology instantly, or use the built-in AI assistant to ask specific questions about injuries, treatments, and damages hidden deep in the file.</p>
            <ul class="hiw-bullets">
                <li> Export straight to Word/PDF</li>
                <li> Direct source citations for every claim</li>
                <li> Chat directly with your documents</li>
            </ul>
        </div>
        <div class="hiw-visual">
            <div class="g-dash">
                <div class="g-table">
                    <div class="g-t-row" style="width: 40%; background:#CBD5E1; margin-bottom: 20px;"></div>
                    <div class="g-t-row"></div>
                    <div class="g-t-row"></div>
                    <div class="g-t-row" style="width: 80%;"></div>
                    <div class="g-t-row"></div>
                </div>
                <div class="g-chat">
                    <div class="g-c-bub"></div>
                    <div class="g-c-bub right"></div>
                    <div class="g-c-bub"></div>
                    <div style="margin-top: auto; height: 20px; background: #1E293B; border-radius: 4px;"></div>
                </div>
            </div>
        </div>
    </div>
</div>
    """, unsafe_allow_html=True)

# 5. Unified Bespoke Pricing Section (Centered & Polished)
    st.markdown("""
<style>
/* Center Wrapper to fix alignment issues */
.center-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    margin-top: 100px;
    margin-bottom: 120px;
}

.cp-section-bespoke {
    background: #FFFFFF;
    border-radius: 32px;
    padding: 80px 60px;
    text-align: center;
    max-width: 1000px; /* Constraints width to keep text readable */
    width: 100%;
    box-shadow: 0 20px 40px -12px rgba(0, 0, 0, 0.06), 0 0 1px rgba(0,0,0,0.1);
    border: 1px solid rgba(255,255,255,0.5);
}

.cp-content-bespoke {
    margin: 0 auto;
}

.cp-tag-bespoke {
    display: inline-block;
    background: #F3F4F6;
    color: #4B5563;
    padding: 8px 18px;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 24px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.cp-title-bespoke {
    font-size: 3.2rem;
    font-weight: 800;
    color: #111827;
    margin-bottom: 20px;
    letter-spacing: -0.04em;
    line-height: 1.1;
}

.cp-desc-bespoke {
    font-size: 1.15rem;
    color: #6B7280;
    max-width: 700px;
    margin-left: auto !important;   /* Force horizontal centering */
    margin-right: auto !important;  /* Force horizontal centering */
    margin-top: 0;
    margin-bottom: 60px;
    line-height: 1.6;
    text-align: center !important;  /* Force the text inside to center */
}

/* Flexbox for even spacing between items */
.cp-vars-bespoke {
    display: flex;
    gap: 40px;
    justify-content: space-between;
    margin-bottom: 70px;
    text-align: center; /* Changed to center for cleaner alignment */
}

.var-item-bespoke {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center; /* Centers icons and text within the item */
}

.var-icon-bespoke {
    width: 52px; height: 52px;
    background: #EFF6FF;
    color: #2563EB;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    margin-bottom: 18px;
}

.var-name-bespoke { font-weight: 700; font-size: 1.1rem; margin-bottom: 8px; color: #111827; }
.var-desc-bespoke { font-size: 0.9rem; color: #6B7280; line-height: 1.5; }

.cp-btn-bespoke {
    display: inline-block;
    background: #000000 !important; /* Pure black for a high-end feel */
    color: #FFFFFF !important;      /* Crisp white text */
    padding: 16px 48px;             /* Slightly tighter padding for modern look */
    border-radius: 999px;           /* Perfect pill shape */
    font-weight: 600;
    font-size: 1.05rem;             /* Slightly smaller for elegance */
    text-decoration: none;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); /* Smoother transition */
    border: 1px solid #000000;      /* Keeps shape crisp */
    cursor: pointer;
}

.cp-btn-bespoke:hover {
    transform: translateY(-2px);    /* Subtle lift */
    background: #1f2937 !important; /* Slight shift to dark charcoal on hover */
    color: #FFFFFF !important;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1); /* Soft, professional shadow */
    border-color: #1f2937;
}
</style>

<div class="center-wrapper">
    <div id="pricing" class="cp-section-bespoke">
        <div class="cp-content-bespoke">
            <div class="cp-tag-bespoke">Tailored Intelligence</div>
            <h2 class="cp-title-bespoke">Bespoke pricing architected <br>for your firm's workflow.</h2>
            <p class="cp-desc-bespoke">
                Legal workloads are unique. Our pricing model reflects your specific volume, case density, and custom data extraction needs.
            </p>
            <div class="cp-vars-bespoke">
                <div class="var-item-bespoke">
                    <div class="var-icon-bespoke">📄</div>
                    <div class="var-name-bespoke">Monthly Page Volume</div>
                    <div class="var-desc-bespoke">Scaling rates based on the total volume of medical records.</div>
                </div>
                <div class="var-item-bespoke">
                    <div class="var-icon-bespoke">📈</div>
                    <div class="var-name-bespoke">Case Load Density</div>
                    <div class="var-desc-bespoke">Structures optimized for high-frequency injury practices.</div>
                </div>
                <div class="var-item-bespoke">
                    <div class="var-icon-bespoke">🎯</div>
                    <div class="var-name-bespoke">Custom Data Points</div>
                    <div class="var-desc-bespoke">Pricing tailored to your firm's specific reporting requirements.</div>
                </div>
            </div>
            <a href="mailto:ishan.parab.comp@gmail.com?subject=Inquiry: Customized Proposal for Green Box Intel" class="cp-btn-bespoke">
                Schedule an Enterprise Assessment
            </a>
        </div>
    </div>
</div>
    """, unsafe_allow_html=True)

    st.markdown("---") # Visual divider

    # Add the Form here
    with st.container():
        st.markdown("<h2 style='text-align: center;'>Request a Customized Proposal</h2>", unsafe_allow_html=True)
        
        # Center the form using columns
        _, form_col, _ = st.columns([1, 2, 1])
        
        with form_col:
            with st.form("client_inquiry", clear_on_submit=True):
                user_email = st.text_input("Work Email")
                user_message = st.text_area("Tell us about your legal document needs")
                
                submit_button = st.form_submit_button("Submit Request")
                
                if submit_button:
                    if user_email and user_message:
                        if send_email(user_email, user_message):
                            st.success("✅ Inquiry sent! We'll contact you soon.")
                        else:
                            st.error("❌ Failed to send. Please check your connection.")
                    else:
                        st.warning("Please fill in both fields.")
            
    # Add spacing at the bottom so you can see the layout
    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- 5. DARK FOOTER ---
    st.markdown(f"""
        <div class="footer-container">
            <div style="display: flex; justify-content: space-between; flex-wrap: wrap; max-width: 1200px; margin: auto;">
                <div style="flex: 1; min-width: 300px; margin-bottom: 40px;">
                    <div class="footer-logo">⚖️ Green Box Intel</div>
                    <p style="max-width: 250px;">AI-powered medical injury document analysis for modern law firms.</p>
                </div>
                <div style="flex: 0.5; min-width: 150px; margin-bottom: 40px;">
                    <h4 style="color: white; margin-bottom: 20px;">Platform</h4>
                    <a href="#how-it-works" class="footer-link">How it Works</a>
                    <a href="#benefits" class="footer-link">Benefits</a>
                    <a href="#pricing" class="footer-link">Pricing</a>
                </div>
                <div style="flex: 0.5; min-width: 150px; margin-bottom: 40px;">
                    <h4 style="color: white; margin-bottom: 20px;">Support</h4>
                    <a href="mailto:ishan.parab.comp@gmail.com" class="footer-link">Contact Sales</a>
                    <a href="#" class="footer-link">Privacy Policy</a>
                    <a href="#" class="footer-link">Terms of Service</a>
                </div>
            </div>
            <div class="footer-bottom" style="max-width: 1200px; margin: auto;">
                <div>© 2026 Green Box Legal. All rights reserved.</div>
                <div>Developed by Ishan Parab</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Add spacing at the bottom so you can see the layout
    st.markdown("<br>", unsafe_allow_html=True)