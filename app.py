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

# ---------- WELCOME PAGE (LOCKED - NOT TOUCHED) ----------
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
        margin-top:10px;
        margin-bottom:20px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        color:white;
        border:none;
        border-radius:10px;
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
                st.session_state.page = "home"
                st.rerun()

    st.stop()

# ---------- GLOBAL STYLE ----------
st.markdown("""
<style>
header {visibility:hidden;}
.block-container {padding-top:1rem;}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #020617, #000000 100%);
    color:white;
}

/* BUTTON FIX (NO WHITE BUTTONS) */
.stButton>button {
    background: linear-gradient(135deg, #00c6ff, #7c3aed);
    color:white;
    border:none;
    border-radius:10px;
    padding:10px 20px;
    font-weight:600;
}

/* HERO */
.hero {
    text-align:center;
    padding:35px;
    border-radius:20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
}

/* CARDS */
.card {
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:15px;
    text-align:center;
    transition:0.3s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow:0 0 20px rgba(0,198,255,0.3);
}

/* INFO BOX */
.info {
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:15px;
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
    st.markdown("<h3>💳 Credit Risk Intelligence</h3>", unsafe_allow_html=True)

with col2:
    if st.button("Logout"):
        st.session_state.user_name = None
        st.rerun()

# ---------- HOME ----------
if st.session_state.page == "home":

    st.markdown(f"""
    <div class="hero">
        <h1>👋 Welcome, {st.session_state.user_name}</h1>
        <p style="color:#aaa;">AI-powered platform for credit risk prediction</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section"></div>', unsafe_allow_html=True)

    # FEATURES
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="card">📊<br><b>Accurate Prediction</b><br>ML insights</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card">⚡<br><b>Real-time Analysis</b><br>Instant results</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card">📈<br><b>Financial Insights</b><br>Better decisions</div>', unsafe_allow_html=True)

    st.markdown('<div class="section"></div>', unsafe_allow_html=True)

    # INFO SECTION (clean + aligned)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="info">
        <h3>🚀 What this app does</h3>
        <ul>
        <li>Predicts loan default risk</li>
        <li>Uses XGBoost model</li>
        <li>Real-time classification</li>
        <li>Supports decision making</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info">
        <h3>🧠 How it works</h3>
        <ol>
        <li>Enter financial data</li>
        <li>Model analyzes</li>
        <li>Get prediction</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Start Prediction"):
        st.session_state.page = "predict"
        st.rerun()

# ---------- PREDICTION ----------
elif st.session_state.page == "predict":

    # BACK BUTTON (NEW)
    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
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
