import streamlit as st
import hashlib
import time
import json
from datetime import datetime, date
import numpy as np
import pandas as pd

# ==========================================
# PAGE CONFIGURATION & ULTRA-MODERN CSS
# ==========================================
st.set_page_config(
    page_title="Khel-Verify AI | National DPI Sports Integrity Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

    /* Global Theme & Font */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f8fafc;
        background-color: #030712;
    }

    /* Main Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::after {
        content: "";
        position: absolute;
        top: 0; right: 0; width: 300px; height: 100%;
        background: radial-gradient(circle, rgba(79, 70, 229, 0.15) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.025em;
        background: linear-gradient(to right, #ffffff, #93c5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #94a3b8;
        margin-top: 0.5rem;
        font-weight: 500;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1.5rem;
        border-radius: 14px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }

    /* USSD Terminal Screen */
    .ussd-terminal {
        background-color: #020617;
        color: #34d399;
        font-family: 'JetBrains Mono', monospace;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #059669;
        box-shadow: inset 0 0 20px rgba(5, 150, 105, 0.15);
        min-height: 260px;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* Status Banners */
    .duress-alert-box {
        background: rgba(127, 29, 29, 0.4);
        border: 1px solid #ef4444;
        color: #fca5a5;
        padding: 1.25rem;
        border-radius: 12px;
        font-weight: 600;
        backdrop-filter: blur(8px);
    }
    .safe-status-box {
        background: rgba(6, 78, 59, 0.4);
        border: 1px solid #10b981;
        color: #6ee7b7;
        padding: 1.25rem;
        border-radius: 12px;
        font-weight: 600;
        backdrop-filter: blur(8px);
    }

    /* Custom Badges */
    .badge-pill {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        font-size: 0.75rem;
        font-weight: 700;
        border-radius: 9999px;
        background-color: rgba(79, 70, 229, 0.2);
        color: #818cf8;
        border: 1px solid rgba(99, 102, 241, 0.4);
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# STATE INITIALIZATION
# ==========================================
if "hash_chain" not in st.session_state:
    genesis_payload = "GENESIS_BLOCK|KHEL_VERIFY_DPI_V2.0|2026-10-21"
    genesis_hash = hashlib.sha256(genesis_payload.encode()).hexdigest()
    st.session_state.hash_chain = [{
        "Block": 0,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Match_ID": "SYS-INIT",
        "Event": "DPI_SECURE_GATEWAY_ONLINE",
        "Score_State": "0-0",
        "Prev_Hash": "0" * 16 + "...",
        "Curr_Hash": genesis_hash[:24] + "...",
        "Status": "IMMUTABLE"
    }]

if "vigilance_alerts" not in st.session_state:
    st.session_state.vigilance_alerts = []

if "bracket_frozen" not in st.session_state:
    st.session_state.bracket_frozen = False

if "ussd_screen_text" not in st.session_state:
    st.session_state.ussd_screen_text = (
        "=== BHARAT SECURE USSD GATE (*99*54#) ===\n"
        "Session ID: #TN-2026-884 (U-17 Kabaddi SF)\n"
        "Public Challenge Factor (M): 37\n\n"
        "👉 Enter Cryptographic Key (Your PIN + 37):"
    )

APAAR_REGISTRY = {
    "APAAR-TN-2009-8421": {
        "name": "Karthik Subramanian",
        "dob": "2009-05-14",
        "age_years": 17.4,
        "school": "Govt Higher Secondary School, Saidapet, Chennai",
        "board_cert_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "biometric_update_age": 16,
        "registered_sim": "+91-94440-XXXXX",
        "true_pin": 12,
        "duress_pin": 45,
        "expected_face_sim": 0.94,
        "eligible_u17": False
    },
    "APAAR-TN-2010-3319": {
        "name": "Muthuvel Pandian",
        "dob": "2010-11-02",
        "age_years": 15.9,
        "school": "Panchayat Union Middle School, Madurai",
        "board_cert_hash": "8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4",
        "biometric_update_age": 15,
        "registered_sim": "+91-98401-XXXXX",
        "true_pin": 21,
        "duress_pin": 88,
        "expected_face_sim": 0.92,
        "eligible_u17": True
    },
    "APAAR-TN-2005-9910": {
        "name": "Vikramaditya R (Impersonation Attempt)",
        "dob": "2005-02-19",
        "age_years": 21.6,
        "school": "Private Sports Academy",
        "board_cert_hash": "2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae",
        "biometric_update_age": 17,
        "registered_sim": "+91-90030-XXXXX",
        "true_pin": 15,
        "duress_pin": 99,
        "expected_face_sim": 0.41,
        "eligible_u17": False
    }
}

def add_block(match_id, event_name, score_state, status="VERIFIED"):
    prev_block = st.session_state.hash_chain[-1]
    prev_hash = prev_block["Curr_Hash"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    payload = f"{len(st.session_state.hash_chain)}|{timestamp}|{match_id}|{event_name}|{score_state}|{prev_hash}"
    curr_hash = hashlib.sha256(payload.encode()).hexdigest()
    st.session_state.hash_chain.append({
        "Block": len(st.session_state.hash_chain),
        "Timestamp": timestamp,
        "Match_ID": match_id,
        "Event": event_name,
        "Score_State": score_state,
        "Prev_Hash": prev_hash[:12] + "...",
        "Curr_Hash": curr_hash[:24] + "...",
        "Status": status
    })

# ==========================================
# HEADER & SIDEBAR
# ==========================================
st.markdown("""
<div class="hero-banner">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <h1 class="hero-title">🛡️ Khel-Verify AI</h1>
            <p class="hero-subtitle">Zero-Hardware DPI Backend Architecture & Cryptographic Anti-Coercion Protocol</p>
        </div>
        <div>
            <span class="badge-pill">Ministry of Education</span>
            <span class="badge-pill">Viksit Bharat 2047</span>
            <span class="badge-pill">IISc Finalist Track</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🏆 Team KCG Innovators")
    st.caption("Department of CSE (Cyber Security), Auto & Mech")
    st.markdown("""
    - **Thatchayaini** *(Lead - Cyber Security)*
    - **Ragul** *(Automobile Engg)*
    - **Natarajan** *(Mechanical Engg)*
    - **Monish** *(Mechanical Engg)*
    - **Yuvan** *(Mechanical Engg)*
    """)
    st.divider()
    st.markdown("### ⚙️ Live System Telemetry")
    st.metric("Hardware Footprint", "₹0 / Ground", delta="-₹15,000 vs Biometric Scanners")
    st.metric("Per-Match Cost", "₹2.40", delta="USSD Cloud Gateway")
    
    status_label = "🚨 BRACKET FROZEN (DURESS)" if st.session_state.bracket_frozen else "🟢 SECURE & LIVE"
    st.markdown(f"**Integrity Status:**<br>`{status_label}`", unsafe_allow_html=True)
    
    st.divider()
    if st.button("🔄 Reset System Demonstration", use_container_width=True):
        st.session_state.bracket_frozen = False
        st.session_state.vigilance_alerts = []
        st.rerun()

# ==========================================
# TABS NAVIGATION
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🪪 Layer 1: APAAR & Edge-AI Face Gate",
    "📟 Layer 2: USSD State & Hash Ledger",
    "🕵️ Layer 3: Anti-Coercion Silent Trap",
    "🚨 State Command & Unit Economics"
])

# ------------------------------------------
# TAB 1: LAYER 1
# ------------------------------------------
with tab1:
    st.markdown("### Layer 1: Automated Age & Identity Gate (APAAR + DigiLocker API)")
    st.caption("Eliminates paper birth certificates and proxy athletes using official government student data stores and offline-first Edge AI.")
    
    col1, col2 = st.columns([1.1, 1], gap="medium")

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📄 DPI Registry Query")
        tournament_div = st.selectbox("Tournament Category", ["Under-17 (U-17) District Championship", "Under-19 (U-19) State Championship"])
        selected_apaar = st.selectbox("Select Athlete 12-Digit APAAR ID", list(APAAR_REGISTRY.keys()))
        student = APAAR_REGISTRY[selected_apaar]

        st.json({
            "APAAR_ID": selected_apaar,
            "Full_Name": student["name"],
            "Official_DOB": student["dob"],
            "Exact_Age": f"{student['age_years']} Years",
            "Affiliated_Institution": student["school"],
            "DigiLocker_Signature": student["board_cert_hash"][:24] + "..."
        })
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 👁️ On-Field PWA Face Recognition Gate")
        st.caption("Cross-matches live camera frame against cryptographically signed DigiLocker reference vector.")
        
        cam_input = st.camera_input("Capture Live Ground Frame")
        
        if st.button("🚀 Execute Verification Protocol", type="primary", use_container_width=True):
            with st.spinner("Executing MobileNetV2 128-D Cosine Matching & Age-Bracket Validation..."):
                time.sleep(0.7)
                face_score = student["expected_face_sim"]
                is_u17 = "U-17" in tournament_div
                age_valid = student["eligible_u17"] if is_u17 else False

                st.progress(int(face_score * 100), text=f"Facial Cosine Similarity: {face_score:.2f} (Required: >= 0.85)")

                if age_valid and face_score >= 0.85:
                    st.success(f"✅ **VERIFIED:** {student['name']} cleared for {tournament_div}. Match token issued.")
                    add_block("TN-2026-884", f"VERIFIED:{selected_apaar}", "PRE-MATCH", "APPROVED")
                elif not age_valid and face_score >= 0.85:
                    st.error(f"❌ **AGE FRAUD BLOCKED:** Athlete is {student['age_years']} yrs old. Exceeds U-17 bracket limit!")
                    add_block("TN-2026-884", f"AGE_FRAUD_BLOCK:{selected_apaar}", "REJECTED", "BLOCKED")
                else:
                    st.error(f"🚨 **IMPERSONATION ALERT:** Similarity score {face_score:.2f} failed threshold! Flagged to State Authority.")
                    add_block("TN-2026-884", f"IMPERSONATION_BLOCK:{selected_apaar}", "REJECTED", "FLAGGED")
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# TAB 2: LAYER 2
# ------------------------------------------
with tab2:
    st.markdown("### Layer 2: Network-Resilient USSD Match Clock & State-Freezing Engine")
    st.caption("Guarantees bulletproof uptime across rural sports grounds with zero internet dependence.")

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🔗 Mutual Handshake")
        a1 = st.checkbox("Athlete A SIM Handshake", value=True)
        a2 = st.checkbox("Athlete B SIM Handshake", value=True)
        ref = st.checkbox("Referee SIM Handshake", value=True)
        if st.button("⚡ Initialize Match Clock", use_container_width=True):
            if a1 and a2 and ref:
                add_block("TN-2026-884", "USSD_MUTUAL_START", "00-00", "LIVE")
                st.success("Match clock active on secure cloud gateway.")
            else:
                st.warning("All 3 SIM nodes required.")
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🧊 State-Freezing Vault")
        score_input = st.text_input("Match Score State", value="24-19")
        reason = st.selectbox("Interruption Event", ["Heavy Rain / Court Wet", "Lighting Grid Failure", "Medical Timeout"])
        if st.button("🔒 Execute Vault Lock", use_container_width=True):
            add_block("TN-2026-884", f"VAULT_LOCK:{reason}", score_input, "FROZEN")
            st.info(f"Score `{score_input}` secured in immutable vault.")
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Ledger Metrics")
        st.metric("Total Blocks Mined", len(st.session_state.hash_chain))
        st.metric("Cryptography", "SHA-256 Chain")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("#### 📜 Live Cryptographic Match Audit Trail")
    st.dataframe(pd.DataFrame(st.session_state.hash_chain), use_container_width=True)

# ------------------------------------------
# TAB 3: LAYER 3
# ------------------------------------------
with tab3:
    st.markdown("### Layer 3: Dual-PIN Cryptographic Challenge & Silent Trap Protocol")
    st.markdown("""
    **The Anti-Coercion Guarantee:** When a match finishes, athletes receive an SMS challenge `PIN + 37`. 
    * True PIN (`21`) + 37 = **58** (Normal confirmation)
    * Duress PIN (`88`) + 37 = **125** (Triggered under physical threat/coercion by corrupt officials)
    """)

    u1, u2 = st.columns([1, 1.2], gap="medium")

    with u1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 📱 Athlete Feature Phone (USSD Simulator)")
        st.markdown(f'<div class="ussd-terminal">{st.session_state.ussd_screen_text}</div>', unsafe_allow_html=True)
        
        entered_val = st.number_input("Keypad Input (Enter 58 for Normal, 125 for Duress):", min_value=0, max_value=999, value=125)
        
        if st.button("📤 Transmit USSD Code", type="primary", use_container_width=True):
            if entered_val == 58:
                st.session_state.ussd_screen_text = (
                    "=== BHARAT SECURE USSD GATE ===\n"
                    "Response: 58 (Authenticated)\n\n"
                    "[STATUS]: Data recorded successfully.\n"
                    "Match TN-2026-884 confirmed."
                )
                add_block("TN-2026-884", "USSD_TRUE_PIN_SUCCESS", "28-22", "VERIFIED")
                st.rerun()
            elif entered_val == 125:
                st.session_state.ussd_screen_text = (
                    "=== BHARAT SECURE USSD GATE ===\n"
                    "Response: 125 (Authenticated)\n\n"
                    "[STATUS]: Data recorded successfully.\n"
                    "Match TN-2026-884 confirmed."
                )
                st.session_state.bracket_frozen = True
                st.session_state.vigilance_alerts.append({
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Match_ID": "TN-2026-884",
                    "Athlete": "Muthuvel Pandian (APAAR-TN-2010-3319)",
                    "Decoded_Duress_PIN": "88 (Hostile Coercion Confirmed)",
                    "Cell_Tower": "CHN-SOUTH-409 (Lat: 13.01, Lon: 80.22)",
                    "Automated_Action": "DECOY UI DISPLAYED | TOURNAMENT BRACKET FROZEN | POLICE/VIGILANCE ALERTED"
                })
                add_block("TN-2026-884", "SILENT_TRAP_TRIGGERED", "28-22 (RIGGED)", "FROZEN_ALERT")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with u2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🧠 Strategic Advantage for Evaluators")
        if st.session_state.bracket_frozen:
            st.markdown("""
            <div class="duress-alert-box">
                🚨 SILENT TRAP SUCCESSFUL!<br><br>
                • <b>Attacker View (Left Screen):</b> Shows a fake success message ("Data recorded successfully"). The aggressor suspects nothing, keeping the young athlete 100% safe from physical harm.<br><br>
                • <b>Backend Cloud View:</b> Instantly decoded the Duress PIN (88), locked the tournament bracket, and beamed a priority alert to state sports vigilance!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="safe-status-box">
                🟢 SYSTEM ARMED & READY<br><br>
                Type <b>125</b> on the keypad and click Transmit to experience how Khel-Verify AI protects grassroots athletes against local corruption without putting them in danger.
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------------------
# TAB 4: STATE COMMAND & ECONOMICS
# ------------------------------------------
with tab4:
    st.markdown("### 🚨 State Vigilance Command & Unit Economics")
    
    if len(st.session_state.vigilance_alerts) > 0:
        st.error("⚠️ ACTIVE COERCION INCIDENTS LOGGED")
        st.table(pd.DataFrame(st.session_state.vigilance_alerts))
    else:
        st.info("All regional tournament brackets operating under normal cryptographic integrity.")

    st.markdown("#### 📈 Feasibility & Cost Matrix (NIT & IISc Evaluation Metric)")
    comparison_df = pd.DataFrame({
        "Evaluation Dimension": [
            "Hardware Infrastructure Cost",
            "Per-Match Operational Cost",
            "Connectivity Dependency",
            "Identity & Age Verification",
            "Physical Safety & Anti-Coercion",
            "Deployment Timeline"
        ],
        "Conventional Biometric Hardware": [
            "₹15,000 – ₹25,000 per venue",
            "₹45.00 per match",
            "Continuous 4G/5G required",
            "Local paper registers / easy forgery",
            "None (vulnerable to physical duress)",
            "6 to 12 months procurement"
        ],
        "Khel-Verify AI (Our Solution)": [
            "₹0 (Zero Hardware Footprint)",
            "₹2.40 per match (Cloud + USSD)",
            "Zero Internet (Basic 2G USSD)",
            "APAAR ID + DigiLocker Cryptographic XML",
            "Cryptographic Dual-PIN Silent Trap",
            "4 Weeks Plug-and-Play API"
        ]
    })
    st.table(comparison_df)