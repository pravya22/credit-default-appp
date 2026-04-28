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

# ---------- WELCOME SCREEN (DO NOT TOUCH) ----------
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

/* CLEAN */
header {visibility:hidden;}
.block-container {padding-top:1rem;}

/* BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #020617, #000000 100%);
    color:white;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #020617;
    padding-top:30px;
}

/* NAV TITLE */
section[data-testid="stSidebar"] h2 {
    color:#00c6ff;
    font-size:20px;
    font-weight:700;
    text-shadow:0 0 12px rgba(0,198,255,0.9);
}

/* NAV ITEMS */
div[role="radiogroup"] > label {
    padding:14px;
    border-radius:14px;
    margin-bottom:10px;
    transition:0.3s;
}

/* HOVER */
div[role="radiogroup"] > label:hover {
    background: rgba(0,198,255,0.15);
    transform: translateX(6px);
}

/* ACTIVE */
div[role="radiogroup"] input:checked + div {
    background: rgba(0,198,255,0.25);
    box-shadow:0 0 15px rgba(0,198,255,0.9);
    border-radius:12px;
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

/* FEATURE CARDS */
.card {
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.08);
    text-align:center;
    transition:0.3s;
}

.card:hover {
    transform: translateY(-6px) scale(1.03);
    box-shadow:0 0 25px rgba(0,198,255,0.3);
}

/* GRADIENT TEXT */
.gradient-text {
    background: linear-gradient(90deg, #00c6ff, #7c3aed, #00c6ff);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: glowMove 5s linear infinite;
}

@keyframes glowMove {
    0% {background-position: 0%;}
    100% {background-position: 200%;}
}

/* INFO CARDS */
.info-card {
    background: rgba(255,255,255,0.05);
    padding:28px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(15px);
    transition:0.4s;
    position:relative;
    box-shadow: inset 0 0 20px rgba(0,198,255,0.05);
}

.info-card:hover {
    transform: translateY(-8px);
    box-shadow:0 0 35px rgba(0,198,255,0.3);
}

/* DIVIDER */
.divider {
    height:2px;
    width:60px;
    margin:10px auto 20px;
    background:linear-gradient(90deg,#00c6ff,#7c3aed);
    box-shadow:0 0 10px rgba(0,198,255,0.8);
    border-radius:10px;
}

/* TEXT */
ul li, ol li {
    margin-bottom:12px;
    line-height:1.6;
    color:#ddd;
}

/* DASHBOARD CARDS */
.dash-card {
    background: rgba(255,255,255,0.05);
    padding:20px;
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.08);
    text-align:center;
    transition:0.3s;
}

.dash-card:hover {
    transform: translateY(-5px);
    box-shadow:0 0 20px rgba(0,198,255,0.3);
}

/* SPACING */
.section {
    margin-top:40px;
}

h1, h2, h3 {
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.markdown("## 🚀 Navigation")
page = st.sidebar.radio("", ["🏠 Home", "📊 Dashboard", "🔍 Prediction"])

if st.sidebar.button("Logout"):
    st.session_state.user_name = None
    st.rerun()

# ---------- HEADER ----------
st.markdown(f"""
<div style="display:flex; justify-content:space-between; padding:10px;
background:rgba(255,255,255,0.05); border-radius:10px;">
<h3>💳 Credit Risk Intelligence</h3>
<p>👋 Hello, {st.session_state.user_name}</p>
</div>
""", unsafe_allow_html=True)

# ---------- HOME ----------
if page == "🏠 Home":

    st.markdown(f"""
    <div class="hero">
        <h1>👋 Welcome, {st.session_state.user_name}</h1>
        <p style="color:#bbb; font-size:16px;">
        AI-powered platform for credit risk prediction
        </p>
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

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="info-card">
            <h2 class="gradient-text">🚀 What this app does</h2>
            <div class="divider"></div>
            <ul>
                <li>✅ Predicts loan default risk using Machine Learning</li>
                <li>🎯 Uses XGBoost model for high accuracy</li>
                <li>⚡ Provides real-time risk classification</li>
                <li>📊 Helps financial decision making</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h2 class="gradient-text">🧠 How it works</h2>
            <div class="divider"></div>
            <ol>
                <li>Enter financial details</li>
                <li>Model analyzes risk factors</li>
                <li>Get instant risk prediction</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

# ---------- DASHBOARD ----------
elif page == "📊 Dashboard":

    import numpy as np

    st.title("📊 Dashboard")

    np.random.seed(42)
    risks = np.random.uniform(0.1, 0.9, 50)

    total = len(risks)
    avg = risks.mean()
    high = (risks > 0.6).sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"<div class='dash-card'><h3>Total Predictions</h3><h2>{total}</h2></div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='dash-card'><h3>High Risk Cases</h3><h2>{high}</h2></div>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<div class='dash-card'><h3>Avg Risk</h3><h2>{avg:.2f}</h2></div>", unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("📉 Risk Distribution")
    st.bar_chart(pd.DataFrame(risks, columns=["Risk Score"]))

# ---------- PREDICTION ----------
elif page == "🔍 Prediction":

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

# ---------- FOOTER ----------
st.markdown("---")
