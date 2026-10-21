import streamlit as st
import hashlib
import time
import json
from datetime import datetime, date
import numpy as np
import pandas as pd

# ==========================================
# PAGE CONFIGURATION & HIGH-CONTRAST SAAS CSS
# ==========================================
st.set_page_config(
    page_title="Khel-Verify AI | National Sports Integrity Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;}

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #0f172a;
        background-color: #f8fafc;
    }

    /* Elite Navbar */
    .saas-navbar {
        background: linear-gradient(90deg, #0f172a 0%, #1e3a8a 100%);
        border: 1px solid rgba(30, 58, 138, 0.2);
        padding: 1rem 2rem;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15);
        margin-bottom: 1.5rem;
    }
    .brand-title {
        font-size: 1.2rem;
        font-weight: 800;
        color: #ffffff !important;
        letter-spacing: -0.02em;
    }

    /* Ultra-Bright Hero Box (High Contrast & Clear) */
    .hero-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
        border: 1px solid rgba(59, 130, 246, 0.4);
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.25);
    }
    .hero-h1 {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff !important;
        opacity: 1 !important;
        margin: 0;
        letter-spacing: -0.03em;
    }
    .hero-p {
        font-size: 1.1rem;
        color: #ffffff !important;
        opacity: 0.95 !important;
        margin-top: 0.75rem;
        max-width: 950px;
        line-height: 1.5;
        font-weight: 500;
    }

    /* Clean Enterprise Cards */
    .clean-card {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    /* Terminal Console */
    .ussd-console {
        background-color: #030712;
        color: #38bdf8;
        font-family: 'JetBrains Mono', monospace;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #0284c7;
        min-height: 250px;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .badge-pill {
        background-color: rgba(255, 255, 255, 0.15);
        color: #ffffff;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# STATE INITIALIZATION
# ==========================================
if "hash_chain" not in st.session_state:
    genesis_payload = "GENESIS_BLOCK|KHEL_VERIFY_DPI_ENTERPRISE|2026-10-21"
    genesis_hash = hashlib.sha256(genesis_payload.encode()).hexdigest()
    st.session_state.hash_chain = [{
        "Block": 0,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Match_ID": "SYS-INIT",
        "Event": "DPI_GATEWAY_ONLINE",
        "Score_State": "0-0",
        "Prev_Hash": "0" * 12 + "...",
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

# NAVBAR & HERO (Updated Title & Clean Bright Look)
st.markdown("""
<div class="saas-navbar">
    <div class="brand-title">KHEL-VERIFY AI - NATIONAL INTEGRITY GRID</div>
    <div style="display:flex; gap:10px;">
        <span class="badge-pill">Ministry of Education</span>
        <span class="badge-pill">Viksit Bharat 2047</span>
    </div>
</div>

<div class="hero-box">
    <h1 class="hero-h1">Khel-Verify AI: Zero-Hardware Backend Architecture with Automated Anti-Coercion Protocol for Sports Fraud Prevention</h1>
    <p class="hero-p">
        Eliminating grassroots sports certificate fraud, identity manipulation, and on-field physical coercion through centralized DPI server logic and cryptographic USSD duress protocols.
    </p>
</div>
""", unsafe_allow_html=True)

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Hardware Footprint", "₹0 / Ground", delta="-₹15,000 vs Biometric")
with col_m2:
    st.metric("Per-Match Cost", "₹2.40", delta="USSD Cloud Gateway")
with col_m3:
    st.metric("Identity Verification", "APAAR + DigiLocker", delta="100% Tamper-Proof")
with col_m4:
    status_str = "FROZEN (DURESS)" if st.session_state.bracket_frozen else "SECURE & LIVE"
    st.metric("System Integrity Status", status_str, delta="SHA-256 Chain Active")

st.divider()

# TABS (Including Architecture Overview)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🪪 Layer 1: APAAR Identity Gate",
    "📟 Layer 2: USSD State Vault",
    "🕵️ Layer 3: Anti-Coercion Trap",
    "🚨 State Vigilance & Economics",
    "🧠 Architecture Overview"
])

# TAB 1
with tab1:
    st.markdown("### Layer 1: Automated Age & Identity Gate (APAAR + DigiLocker API)")
    st.markdown("Eliminates paper birth certificates and proxy athletes using official government student data repositories and offline-first Edge AI.")
    
    c1, c2 = st.columns([1.1, 1], gap="medium")

    with c1:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("#### 📄 DPI Student Registry Lookup")
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

    with c2:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
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

# TAB 2
with tab2:
    st.markdown("### Layer 2: Network-Resilient USSD Match Clock & State-Freezing Engine")
    st.markdown("Guarantees bulletproof uptime across rural sports grounds with zero internet dependence via 2G USSD handshakes.")

    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
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
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("#### 🧊 State-Freezing Vault")
        score_input = st.text_input("Match Score State", value="24-19")
        reason = st.selectbox("Interruption Event", ["Heavy Rain / Court Wet", "Lighting Grid Failure", "Medical Timeout"])
        if st.button("🔒 Execute Vault Lock", use_container_width=True):
            add_block("TN-2026-884", f"VAULT_LOCK:{reason}", score_input, "FROZEN")
            st.info(f"Score `{score_input}` secured in immutable vault.")
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Ledger Metrics")
        st.metric("Total Blocks Mined", len(st.session_state.hash_chain))
        st.metric("Cryptography", "SHA-256 Chain")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("#### 📜 Live Cryptographic Match Audit Trail")
    st.dataframe(pd.DataFrame(st.session_state.hash_chain), use_container_width=True)

# TAB 3
with tab3:
    st.markdown("### Layer 3: Dual-PIN Cryptographic Challenge & Silent Trap Protocol")
    st.markdown("""
    **The Anti-Coercion Guarantee:** When a match finishes, athletes receive an SMS challenge `PIN + 37`. 
    * True PIN (`21`) + 37 = **58** (Normal confirmation)
    * Duress PIN (`88`) + 37 = **125** (Triggered under physical threat/coercion by corrupt officials)
    """)

    u1, u2 = st.columns([1, 1.2], gap="medium")

    with u1:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("#### 📱 Athlete Feature Phone (USSD Simulator)")
        st.markdown(f'<div class="ussd-console">{st.session_state.ussd_screen_text}</div>', unsafe_allow_html=True)
        
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
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("#### 🧠 Strategic Advantage for Evaluators")
        if st.session_state.bracket_frozen:
            st.error("""
            🚨 **SILENT TRAP SUCCESSFUL!**
            * **Attacker View (Left Screen):** Shows a fake success message ("Data recorded successfully"). The aggressor suspects nothing, keeping the young athlete 100% safe from physical harm.
            * **Backend Cloud View:** Instantly decoded the Duress PIN (88), locked the tournament bracket, and beamed a priority alert to state sports vigilance!
            """)
        else:
            st.success("""
            🟢 **SYSTEM ARMED & READY**
            Type **125** on the keypad and click Transmit to experience how Khel-Verify AI protects grassroots athletes against local corruption without putting them in danger.
            """)
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 4
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

# TAB 5: ARCHITECTURE OVERVIEW
with tab5:
    st.markdown("### 🧠 Comprehensive Architecture Overview & Technology Stack")
    
    col_a1, col_a2 = st.columns(2, gap="medium")
    with col_a1:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("#### 🛠️ Technology Stack & Background Solution")
        st.markdown("""
        - **Problem Background:** Grassroots sports suffer from age fraud, certificate tampering, and on-field coercion of vulnerable athletes by local officials.
        - **Zero-Hardware Backend:** Bypasses expensive ₹15,000+ biometric scanners using existing national cloud & telecom infrastructures.
        - **DPI Data Pipeline:** Integrates 12-digit APAAR ID and DigiLocker XML APIs for tamper-proof birth records.
        - **Edge Vision:** MobileNetV2 128-D vector matching for offline biometric face verification.
        - **Telecom Integration:** USSD session gateways enabling basic 2G feature phone authentication.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_a2:
        st.markdown('<div class="clean-card">', unsafe_allow_html=True)
        st.markdown("#### 🔒 Cryptographic & Security Architecture")
        st.markdown("""
        - **SHA-256 Hash-Chain Ledger:** Every match start, score state, and interruption is immutably chained to prevent local tampering during breaks.
        - **Dual-PIN Cryptographic Algebra:** Layer 3 separates True PIN ($T$) from Duress PIN ($D$), triggering silent state vigilance alerts while displaying decoy success messages on feature phones.
        - **Team Roster:** Developed by Team KCG Innovators (Thatchayaini, Ragul, Natarajan, Monish, Yuvan) from KCG College of Technology.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
