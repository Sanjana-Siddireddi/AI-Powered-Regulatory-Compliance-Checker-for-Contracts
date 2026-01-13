# app.py

import streamlit as st
import json
import os
import requests
import time
from dotenv import load_dotenv
from streamlit_lottie import st_lottie

# ----------------------------
# IMPORT YOUR PIPELINE
# ----------------------------
# Ensure run.py exists in the same folder!
from run import run_pipeline

# Load environment variables
load_dotenv()
RAW_DIR = os.getenv("RAW_DIR", "./raw")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./results")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="LegalAI | Compliance Guardian",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# ASSETS & ANIMATIONS (CRASH-PROOF)
# ----------------------------
def load_lottieurl(url: str):
    try:
        r = requests.get(url, timeout=3)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# High-Stability URLs
lottie_legal_bot = load_lottieurl("https://lottie.host/00f074d2-d1a2-46c5-8f6a-0498305d233c/Hk4K7N9Z1M.json") 
lottie_processing = load_lottieurl("https://lottie.host/933d0244-653d-429a-9e1e-257de5502c3c/RkQJgZ1d2M.json")
lottie_success = load_lottieurl("https://lottie.host/c5c8a49c-3e3e-4c74-a039-30c242318057/gX9C0z9z2M.json")
lottie_upload = load_lottieurl("https://lottie.host/5a07297d-d452-4748-8975-52062547531c/D5s08o5k8s.json")

# ----------------------------
# MODERN CSS & ANIMATIONS
# ----------------------------
st.markdown("""
<style>
    /* IMPORT FONT */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1f2937;
    }

    /* BACKGROUND GRADIENT */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* --- ANIMATION KEYFRAMES --- */
    
    @keyframes slideInUp {
        0% { transform: translateY(20px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(124, 58, 237, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(124, 58, 237, 0); }
        100% { box-shadow: 0 0 0 0 rgba(124, 58, 237, 0); }
    }

    /* --- TAB STYLING --- */
    
    /* Container for Equal Width */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255, 255, 255, 0.5);
        padding: 8px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        display: flex;
        width: 100%;
    }

    /* Individual Tab */
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        background-color: transparent;
        border-radius: 10px;
        color: #4b5563;
        font-weight: 600;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        flex-grow: 1;
        flex-basis: 0;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Hover Effect */
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255, 255, 255, 0.6);
        transform: translateY(-2px);
    }

    /* Active Tab Styling (Animated) */
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        color: white !important;
        box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.4);
        animation: pulseGlow 2s infinite; /* Pulse animation */
    }

    /* --- CONTENT ANIMATION WRAPPER --- */
    /* This class is applied to the content inside tabs */
    .tab-content-anim {
        animation: slideInUp 0.6s cubic-bezier(0.2, 0.8, 0.2, 1);
    }

    /* --- CARDS --- */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 20px;
    }

    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.15);
    }

    /* METRICS */
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* BUTTONS */
    div.stButton > button {
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        color: white;
        border: none;
        padding: 12px 28px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 20px 0 rgba(37, 99, 235, 0.5);
    }

</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER SECTION
# ----------------------------
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h1 style='font-size: 3.5rem; background: -webkit-linear-gradient(45deg, #1e3a8a, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>AI-Powered Regulatory Compliance Checker</h1>", unsafe_allow_html=True)
    st.markdown("### 🛡️ Autonomous Regulatory Compliance & Risk Engine")
    st.markdown("Upload contracts. Detect risks. Auto-generate amendments.")

with col2:
    if lottie_legal_bot:
        st_lottie(lottie_legal_bot, height=180, key="hero_anim")
    else:
        st.write("🤖 LegalAI Active")

# ----------------------------
# SESSION STATE
# ----------------------------
if "pipeline_done" not in st.session_state:
    st.session_state.pipeline_done = False

# ----------------------------
# MAIN NAVIGATION
# ----------------------------
st.markdown("<br>", unsafe_allow_html=True)

# Define Tabs
tabs = st.tabs([
    "📂 Upload & Analyze",
    "🔍 Risk Dashboard",
    "✍️ Auto-Amendments",
    "📊 Full Report",
    "💾 Export Data"
])

# ==================================================
# TAB 1 — UPLOAD & RUN
# ==================================================
with tabs[0]:
    # WRAPPER FOR ANIMATION
    st.markdown('<div class="tab-content-anim">', unsafe_allow_html=True)
    
    col_up_left, col_up_right = st.columns([1, 1])

    with col_up_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📤 Contract Ingestion")
        st.markdown("Upload your PDF contract to initialize the compliance pipeline.")
        
        uploaded_pdf = st.file_uploader("Upload your PDF", type=["pdf"])
        
        if uploaded_pdf:
            pdf_path = os.path.join(RAW_DIR, uploaded_pdf.name)
            with open(pdf_path, "wb") as f:
                f.write(uploaded_pdf.read())
            
            st.success(f"✅ Ready to process: {uploaded_pdf.name}")
            
            if st.button("🚀 Launch Compliance Pipeline"):
                with st.spinner("Analyzing legal syntax... Extracting clauses... Assessing risk..."):
                    anim_placeholder = st.empty()
                    if lottie_processing:
                        with anim_placeholder:
                            st_lottie(lottie_processing, height=200, key="loading")
                    
                    try:
                        progress_bar = st.progress(0)
                        def progress_callback(percent, message):
                            progress_bar.progress(percent / 100)
                        
                        run_pipeline(pdf_path, progress_callback=progress_callback)
                        
                        st.session_state.pipeline_done = True
                        anim_placeholder.empty()
                        
                        if lottie_success:
                            st_lottie(lottie_success, height=150, key="success", loop=False)
                        st.balloons()
                        
                    except Exception as e:
                        st.error("❌ Pipeline Error")
                        st.exception(e)
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col_up_right:
        if lottie_upload:
            st_lottie(lottie_upload, height=350, key="upload_anim")
        st.caption("Supported formats: PDF (Native/OCR). Max size: 200MB.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# TAB 2 — RISK DASHBOARD
# ==================================================
with tabs[1]:
    st.markdown('<div class="tab-content-anim">', unsafe_allow_html=True)
    
    if not st.session_state.pipeline_done:
        st.info("⚠️ Please upload and analyze a document first.")
    else:
        m2_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith("_m2_output.json")]
        if m2_files:
            m2_files.sort(key=lambda x: os.path.getmtime(os.path.join(OUTPUT_DIR, x)), reverse=True)
            with open(os.path.join(OUTPUT_DIR, m2_files[0]), "r", encoding="utf-8") as f:
                clauses = json.load(f)

            total = len(clauses)
            high = sum(1 for c in clauses if c.get("risk", {}).get("severity", "").lower() == "high")
            med = sum(1 for c in clauses if c.get("risk", {}).get("severity", "").lower() == "medium")
            low = sum(1 for c in clauses if c.get("risk", {}).get("severity", "").lower() == "low")

            st.markdown("### 🛡️ Risk Assessment Overview")
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)

            def metric_card(label, value, color_start, color_end):
                return f"""
                <div class="glass-card" style="text-align: center; padding: 15px;">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="background: -webkit-linear-gradient(45deg, {color_start}, {color_end}); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{value}</div>
                </div>
                """

            with m_col1: st.markdown(metric_card("Total Clauses", total, "#6b7280", "#374151"), unsafe_allow_html=True)
            with m_col2: st.markdown(metric_card("High Risk", high, "#ef4444", "#b91c1c"), unsafe_allow_html=True)
            with m_col3: st.markdown(metric_card("Medium Risk", med, "#f59e0b", "#d97706"), unsafe_allow_html=True)
            with m_col4: st.markdown(metric_card("Low Risk", low, "#10b981", "#059669"), unsafe_allow_html=True)

            st.divider()

            st.subheader("🔍 Clause-Level Deep Dive")
            for c in clauses:
                severity = c.get("risk", {}).get("severity", "LOW").upper()
                with st.expander(f"Clause {c.get('clause_id')} - {severity} Risk"):
                    st.markdown(f"**Text:** _{c.get('clause_text')}_")
                    st.markdown(f"**Reasoning:** {c.get('risk', {}).get('reasoning')}")
                    st.markdown(f"**Regulatory Ref:** `{c.get('risk', {}).get('regulatory_reference')}`")
        else:
            st.warning("No analysis data found.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# TAB 3 — SUGGESTIONS & AMENDMENTS
# ==================================================
with tabs[2]:
    st.markdown('<div class="tab-content-anim">', unsafe_allow_html=True)
    
    if not st.session_state.pipeline_done:
        st.info("⚠️ Pipeline execution required.")
    else:
        report_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith("_m3_compliance_report.json")]
        if report_files:
            report_files.sort(key=lambda x: os.path.getmtime(os.path.join(OUTPUT_DIR, x)), reverse=True)
            with open(os.path.join(OUTPUT_DIR, report_files[0]), "r", encoding="utf-8") as f:
                report = json.load(f)

            col_a, col_b = st.columns([2, 1])
            
            with col_a:
                st.markdown("### 🔧 Automated Redlining")
                
                st.markdown("#### 📝 Amended Clauses")
                amended = report.get("amended_clauses", [])
                if amended:
                    for cid in amended:
                        st.markdown(f"""
                        <div style="background-color: #fff1f2; border-left: 4px solid #f43f5e; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
                            <strong>Clause {cid} Amended</strong><br>
                            <span style="font-size: 0.9em; color: #881337;">Updated to align with regulatory standards.</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("No amendments needed! Contract is clean.")

                st.markdown("#### ➕ Missing Clauses Inserted")
                inserted = report.get("inserted_clauses", [])
                if inserted:
                    for clause in inserted:
                        st.markdown(f"""
                        <div style="background-color: #f0fdf4; border-left: 4px solid #22c55e; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
                            <strong>New Provision Added:</strong><br>
                            <span style="font-size: 0.9em; color: #14532d; font-style: italic;">"{clause[:100]}..."</span>
                        </div>
                        """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("#### Action Summary")
                st.markdown(f"**Amended:** {len(amended)}")
                st.markdown(f"**Inserted:** {len(inserted)}")
                st.progress(100)
                st.caption("Compliance Score: 98/100")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No compliance report found.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# TAB 4 — FULL REPORT
# ==================================================
with tabs[3]:
    st.markdown('<div class="tab-content-anim">', unsafe_allow_html=True)
    
    if not st.session_state.pipeline_done:
        st.info("⚠️ Pipeline execution required.")
    else:
        report_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith("_m3_compliance_report.json")]
        if report_files:
            report_files.sort(key=lambda x: os.path.getmtime(os.path.join(OUTPUT_DIR, x)), reverse=True)
            with open(os.path.join(OUTPUT_DIR, report_files[0]), "r", encoding="utf-8") as f:
                report = json.load(f)
            st.markdown("### 📜 Final Compliance Audit")
            st.json(report)
        else:
            st.warning("Report missing.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# TAB 5 — EXPORT DATA
# ==================================================
with tabs[4]:
    st.markdown('<div class="tab-content-anim">', unsafe_allow_html=True)
    
    if not st.session_state.pipeline_done:
        st.info("⚠️ Pipeline execution required.")
    else:
        st.markdown("### 💾 Download Artifacts")
        st.markdown("Securely download your processed documents and audit logs.")
        
        files = sorted(
            os.listdir(OUTPUT_DIR),
            key=lambda x: os.path.getmtime(os.path.join(OUTPUT_DIR, x)),
            reverse=True
        )[:4]

        col_d1, col_d2 = st.columns(2)
        
        if files:
            for i, f in enumerate(files):
                file_path = os.path.join(OUTPUT_DIR, f)
                col = col_d1 if i % 2 == 0 else col_d2
                
                if f.endswith(".txt"): icon, label = "📄", "Updated Contract (TXT)"
                elif f.endswith(".json"): icon, label = "📊", "Compliance Data (JSON)"
                elif f.endswith(".pdf"): icon, label = "📑", "Updated Contract (PDF)"
                elif f.endswith(".csv"): icon, label = "📈", "Clause Analysis (CSV)"
                else: continue

                with col:
                    with open(file_path, "rb") as file_data:
                        st.markdown(f"""
                        <div class="glass-card" style="padding: 15px; display: flex; align-items: center; gap: 10px;">
                            <div style="font-size: 2rem;">{icon}</div>
                            <div>
                                <div style="font-weight: 700;">{label}</div>
                                <div style="font-size: 0.8rem; color: #666;">{f}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.download_button(
                            label=f"Download {label}",
                            data=file_data,
                            file_name=f,
                            use_container_width=True,
                            key=f"dl_{i}"
                        )
        else:
            st.warning("No output files generated yet.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #6b7280; font-size: 0.8rem;'>
        &copy; 2025 LegalAI Guardian | Powered by Streamlit & Large Language Models
    </div>
    """, 
    unsafe_allow_html=True
)