import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Page config
st.set_page_config(page_title="Credit Risk Intelligence", page_icon="💳", layout="wide")

# ---------- SESSION ----------
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# ---------- WELCOME SCREEN (UNCHANGED) ----------
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
        white-space: nowrap;
    }

    .subtitle {
        color:#aaa;
        font-size:15px;
        margin-top:10px;
        margin-bottom:20px;
    }

    .stTextInput>div>div>input {
        text-align:center;
    }

    .stButton>button {
        width:140px;
        border-radius:10px;
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        color:white;
        border:none;
        padding:10px;
        display:block;
        margin:auto;
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

        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            name = st.text_input("", placeholder="Enter your name")

        c4, c5, c6 = st.columns([1,1,1])
        with c5:
            if st.button("Enter"):
                if name.strip():
                    st.session_state.user_name = name
                    st.rerun()

    st.stop()

# ---------- GLOBAL UI ----------
st.markdown("""
<style>

/* REMOVE EXTRA SPACE */
header {visibility:hidden;}
.block-container {padding-top:1rem;}

/* BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #020617, #000000 100%);
    color:white;
}

/* 🔥 BUTTON FIX (ONLY CHANGE) */
.stButton > button {
    background: linear-gradient(135deg, #00c6ff, #0072ff) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 18px !important;
    font-weight: 600 !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #0096c7, #005bea) !important;
    box-shadow: 0 0 10px rgba(0,198,255,0.6);
}

/* 🔥 LABEL FIX */
label {
    color: white !important;
    font-weight: 600 !important;
}

/* KEEP YOUR ORIGINAL DESIGN */
.hero {
    text-align:center;
    padding:30px;
    border-radius:20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border:1px solid rgba(255,255,255,0.08);
}

.card {
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.08);
    text-align:center;
    transition:0.3s;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow:0 0 25px rgba(0,198,255,0.25);
}

.section {
    margin-top:40px;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown(f"""
<div style="display:flex; justify-content:space-between; padding:10px;
background:rgba(255,255,255,0.05); border-radius:10px;">
<h3>💳 Credit Risk Intelligence</h3>
<p>👋 Hello, {st.session_state.user_name}</p>
</div>
""", unsafe_allow_html=True)

# ---------- HOME (UNCHANGED) ----------
st.markdown(f"""
<div class="hero">
    <h1>👋 Welcome, {st.session_state.user_name}</h1>
    <p style="color:#aaa;">AI-powered platform for credit risk prediction</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section"></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">📊<br><b>Accurate Prediction</b><br>ML powered insights</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">⚡<br><b>Real-time Analysis</b><br>Instant results</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">📈<br><b>Financial Insights</b><br>Better decisions</div>', unsafe_allow_html=True)

st.markdown('<div class="section"></div>', unsafe_allow_html=True)

# ---------- PREDICTION (UNCHANGED) ----------
st.title("🔍 Credit Risk Prediction")

col1, col2 = st.columns(2)

with col1:
    debt = st.number_input("Debt Ratio", min_value=0.0, value=0.5)
    income = st.number_input("Monthly Income", min_value=0.0, value=5000.0)

with col2:
    late = st.number_input("Late Payments (90 days)", min_value=0, value=0)
    util = st.number_input("Credit Utilization", min_value=0.0, value=0.3)

input_df = pd.DataFrame([{
    "DebtRatio": debt,
    "MonthlyIncome": income,
    "NumberOfTimes90DaysLate": late,
    "RevolvingUtilizationOfUnsecuredLines": util
}])

if st.button("Predict Risk"):

    probability = model.predict_proba(input_df)[0][1]

    if probability < 0.3:
        st.success("Low Risk")
    elif probability < 0.6:
        st.warning("Medium Risk")
    else:
        st.error("High Risk")

    st.progress(float(probability))
    st.metric("Default Probability", f"{probability:.2f}")
