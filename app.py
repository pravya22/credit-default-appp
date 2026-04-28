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

# ---------- WELCOME ----------
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
        text-shadow: 0 0 15px rgba(0,255,255,0.7);
    }
    .stTextInput input {
        text-align:center;
    }
    .stButton button {
        width:140px;
        border-radius:10px;
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        color:white;
        border:none;
        display:block;
        margin:auto;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass">
        <div class="title">💳 Credit Risk Intelligence</div>
        <p style="color:#aaa;">AI-powered risk analysis</p>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input("", placeholder="Enter your name")

    if st.button("Enter"):
        if name.strip():
            st.session_state.user_name = name
            st.session_state.page = "home"
            st.rerun()

    st.stop()

# ---------- GLOBAL UI ----------
st.markdown("""
<style>
header {visibility:hidden;}
.block-container {padding-top:1rem;}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #020617, #000000 100%);
    color:white;
}
.hero {
    text-align:center;
    padding:30px;
    border-radius:20px;
    background: rgba(255,255,255,0.05);
}
.card {
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:18px;
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER WITH LOGOUT ----------
col1, col2 = st.columns([8,1])

with col1:
    st.markdown(f"<h3>💳 Credit Risk Intelligence</h3>", unsafe_allow_html=True)

with col2:
    if st.button("Logout"):
        st.session_state.user_name = None
        st.session_state.page = "home"
        st.rerun()

# ---------- HOME PAGE ----------
if st.session_state.page == "home":

    st.markdown(f"""
    <div class="hero">
        <h1>👋 Welcome, {st.session_state.user_name}</h1>
        <p style="color:#bbb;">AI-powered credit risk platform</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
        <h3>🚀 What this app does</h3>
        <p>Predicts loan default risk using Machine Learning</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h3>🧠 How it works</h3>
        <p>Enter details → Model analyzes → Get prediction</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 🔥 START BUTTON
    if st.button("🚀 Start Prediction"):
        st.session_state.page = "predict"
        st.rerun()

# ---------- PREDICTION PAGE ----------
elif st.session_state.page == "predict":

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

        prob = model.predict_proba(input_df)[0][1]

        if prob < 0.3:
            st.success("Low Risk")
        elif prob < 0.6:
            st.warning("Medium Risk")
        else:
            st.error("High Risk")

        st.metric("Probability", f"{prob:.2f}")
        st.progress(float(prob))
