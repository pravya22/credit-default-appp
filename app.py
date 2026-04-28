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

# ---------- GLOBAL UI ----------
st.markdown("""
<style>

/* BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #020617, #000000 100%);
    color:white;
}

/* FIX BUTTONS */
.stButton>button {
    background: linear-gradient(135deg, #00c6ff, #0072ff) !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 10px 18px !important;
    font-weight:600;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 12px rgba(0,198,255,0.6);
}

/* FIX LABEL VISIBILITY */
label {
    color: white !important;
    font-weight:600 !important;
}

/* CARDS */
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
    box-shadow:0 0 25px rgba(0,198,255,0.3);
}

/* INFO BOX */
.info-card {
    background: rgba(255,255,255,0.05);
    padding:28px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(15px);
}

/* SPACING */
.section {
    margin-top:40px;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
col1, col2 = st.columns([8,1])

with col1:
    st.markdown("### 💳 Credit Risk Intelligence")

with col2:
    if st.button("Logout"):
        st.session_state.user_name = None
        st.rerun()

# ---------- HOME (RESTORED) ----------
st.markdown(f"""
<h1>👋 Welcome, {st.session_state.user_name}</h1>
<p style="color:#bbb;">AI-powered platform for credit risk prediction</p>
""", unsafe_allow_html=True)

st.markdown('<div class="section"></div>', unsafe_allow_html=True)

# FEATURES
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="card">📊<br><b>Accurate Prediction</b><br>ML powered insights</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">⚡<br><b>Real-time Analysis</b><br>Instant results</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="card">📈<br><b>Financial Insights</b><br>Better decisions</div>', unsafe_allow_html=True)

st.markdown('<div class="section"></div>', unsafe_allow_html=True)

# INFO SECTION
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
    <h2>🚀 What this app does</h2>
    <ul>
    <li>Predicts loan default risk using Machine Learning</li>
    <li>Uses XGBoost model</li>
    <li>Provides real-time classification</li>
    <li>Helps decision making</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
    <h2>🧠 How it works</h2>
    <ol>
    <li>Enter financial details</li>
    <li>Model analyzes data</li>
    <li>Get instant prediction</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section"></div>', unsafe_allow_html=True)

# BUTTON TO PREDICTION
if st.button("🚀 Start Prediction"):
    st.session_state.show_prediction = True

# ---------- PREDICTION ----------
if st.session_state.get("show_prediction", False):

    if st.button("⬅ Back to Home"):
        st.session_state.show_prediction = False
        st.rerun()

    st.title("🔍 Credit Risk Prediction")

    col1, col2 = st.columns(2)

    with col1:
        debt = st.number_input("Debt Ratio", 0.0, 1.0, 0.5)
        income = st.number_input("Monthly Income", 0.0, 100000.0, 5000.0)

    with col2:
        late = st.number_input("Late Payments", 0, 10, 0)
        util = st.number_input("Credit Utilization", 0.0, 1.0, 0.3)

    input_df = pd.DataFrame([{
        "DebtRatio": debt,
        "MonthlyIncome": income,
        "NumberOfTimes90DaysLate": late,
        "RevolvingUtilizationOfUnsecuredLines": util
    }])

    if st.button("Predict Risk"):

        prob = model.predict_proba(input_df)[0][1]

        if prob < 0.3:
            st.success("Low Risk")
        elif prob < 0.6:
            st.warning("Medium Risk")
        else:
            st.error("High Risk")

        st.progress(float(prob))
        st.metric("Default Probability", f"{prob:.2f}")
