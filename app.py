import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="Credit Risk Intelligence", page_icon="💳", layout="wide")

# ---------- SESSION ----------
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------- WELCOME PAGE (100% SAME - NOT TOUCHED) ----------
if st.session_state.user_name is None:

    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, black 80%);
    }

    .glass {
        background: rgba(255,255,255,0.05);
        padding:25px;
        border-radius:20px;
        backdrop-filter: blur(12px);
        border:1px solid rgba(255,255,255,0.1);
        text-align:center;
    }

    .title {
        font-size:40px;
        font-weight:800;
        color:white;
        text-shadow: 0 0 15px rgba(0,255,255,0.7),
                     0 0 30px rgba(0,255,255,0.4);
    }

    .subtitle {
        color:#aaa;
        font-size:15px;
        margin-top:10px;
        margin-bottom:20px;
    }

    .stButton>button {
        width:140px;
        border-radius:10px;
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        color:white;
        border:none;
        padding:10px;
        margin:auto;
        display:block;
    }
    </style>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1,2,1])

    with center:
        st.markdown("""
        <div class="glass">
            <div class="title">💳 Credit Risk Intelligence</div>
            <div class="subtitle">Welcome to AI-powered risk analysis</div>
        </div>
        """, unsafe_allow_html=True)

        name = st.text_input("", placeholder="Enter your name")

        if st.button("Enter"):
            if name.strip():
                st.session_state.user_name = name
                st.rerun()

    st.stop()

# ---------- GLOBAL DARK UI (RESTORE YOUR ORIGINAL LOOK) ----------
st.markdown("""
<style>

/* BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #020617, #000000 100%);
    color:white;
}

/* TEXT */
h1,h2,h3,h4,h5,p,label {
    color:white !important;
}

/* HEADER */
.header {
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:10px;
    background:rgba(255,255,255,0.05);
    border-radius:10px;
}

/* HERO */
.hero {
    text-align:center;
    padding:30px;
    border-radius:20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border:1px solid rgba(255,255,255,0.08);
}

/* CARDS */
.card {
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.08);
    text-align:center;
}

/* INFO CARDS */
.info-card {
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.08);
}

/* BUTTONS */
.stButton>button {
    border-radius:12px;
    background: linear-gradient(135deg, #00c6ff, #7c3aed);
    color:white;
    border:none;
    padding:10px 18px;
    font-weight:600;
}

/* RESULT BOX */
.result-box {
    text-align:center;
    padding:25px;
    border-radius:20px;
    margin-top:20px;
    background: rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.1);
}

/* COLORS */
.low {color:#22c55e;}
.medium {color:#facc15;}
.high {color:#ef4444;}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
col1, col2 = st.columns([6,1])
with col1:
    st.markdown("### 💳 Credit Risk Intelligence")
with col2:
    if st.button("Logout"):
        st.session_state.user_name = None
        st.session_state.page = "home"
        st.rerun()

# ---------- HOME PAGE (RESTORED PROPERLY) ----------
if st.session_state.page == "home":

    st.markdown(f"""
    <div class="hero">
        <h1>👋 Welcome, {st.session_state.user_name}</h1>
        <p>AI-powered platform for credit risk prediction</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">📊<br><b>Accurate Prediction</b><br>ML insights</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="card">⚡<br><b>Real-time Analysis</b><br>Instant results</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="card">📈<br><b>Financial Insights</b><br>Better decisions</div>', unsafe_allow_html=True)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="info-card">
        <h3>🚀 What this app does</h3>
        <ul>
        <li>Predicts loan default risk</li>
        <li>Uses ML model</li>
        <li>Real-time classification</li>
        <li>Helps decision making</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
        <h3>🧠 How it works</h3>
        <ol>
        <li>Enter financial data</li>
        <li>Model analyzes</li>
        <li>Get prediction</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    if st.button("🚀 Start Prediction"):
        st.session_state.page = "prediction"
        st.rerun()

# ---------- PREDICTION PAGE ----------
elif st.session_state.page == "prediction":

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.title("🔍 Credit Risk Prediction")

    col1, col2 = st.columns(2)

    with col1:
        debt = st.number_input("Debt Ratio", value=0.5)
        income = st.number_input("Monthly Income", value=5000.0)

    with col2:
        late = st.number_input("Late Payments", value=0)
        util = st.number_input("Credit Utilization", value=0.3)

    input_df = pd.DataFrame([{
        "DebtRatio": debt,
        "MonthlyIncome": income,
        "NumberOfTimes90DaysLate": late,
        "RevolvingUtilizationOfUnsecuredLines": util
    }])

    if st.button("Predict Risk"):

        probability = model.predict_proba(input_df)[0][1]

        if probability < 0.3:
            risk = "LOW RISK"
            cls = "low"
        elif probability < 0.6:
            risk = "MEDIUM RISK"
            cls = "medium"
        else:
            risk = "HIGH RISK"
            cls = "high"

        st.markdown(f"""
        <div class="result-box">
            <h2 class="{cls}">{risk}</h2>
            <h1>{probability:.2f}</h1>
        </div>
        """, unsafe_allow_html=True)

        st.progress(float(probability))
