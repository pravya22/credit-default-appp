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
    st.session_state.page = "welcome"


# ---------- GLOBAL CSS ----------
st.markdown("""
<style>

header {visibility:hidden;}
.block-container {padding-top:1rem;}

/* DARK BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #020617, #000000);
    color: white;
}

/* BUTTON FIX */
.stButton > button {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: 600;
    box-shadow: 0 0 10px rgba(0,198,255,0.5);
}

.stButton > button:hover {
    box-shadow: 0 0 20px rgba(0,198,255,1);
}

/* INPUT LABEL FIX */
label {
    color: #e5e7eb !important;
}

/* GLASS CARD */
.glass {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    border:1px solid rgba(255,255,255,0.1);
}

/* CENTER */
.center {
    text-align:center;
}

</style>
""", unsafe_allow_html=True)


# ---------- 1️⃣ WELCOME PAGE ----------
if st.session_state.page == "welcome":

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.markdown("""
        <div class="glass center">
            <h1>💳 Credit Risk Intelligence</h1>
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


# ---------- HEADER ----------
st.markdown(f"""
<div style="display:flex; justify-content:space-between; padding:10px;
background:rgba(255,255,255,0.05); border-radius:10px;">
<h3>💳 Credit Risk Intelligence</h3>
<p>👋 {st.session_state.user_name}</p>
</div>
""", unsafe_allow_html=True)


# ---------- LOGOUT ----------
colA, colB = st.columns([8,1])
with colB:
    if st.button("Logout"):
        st.session_state.user_name = None
        st.session_state.page = "welcome"
        st.rerun()


# ---------- 2️⃣ HOME PAGE ----------
if st.session_state.page == "home":

    st.markdown(f"""
    <div class="glass center">
        <h1>👋 Welcome, {st.session_state.user_name}</h1>
        <p style="color:#aaa;">AI-powered platform for credit risk prediction</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🚀 What this app does")
    st.markdown("""
- Predicts loan default risk using Machine Learning  
- Uses XGBoost model for high accuracy  
- Provides real-time risk classification  
- Helps financial decision making  
""")

    st.markdown("### 🧠 How it works")
    st.markdown("""
1. Enter financial details  
2. Model analyzes risk  
3. Get instant prediction  
""")

    st.markdown("")

    if st.button("🚀 Start Prediction"):
        st.session_state.page = "prediction"
        st.rerun()


# ---------- 3️⃣ PREDICTION PAGE ----------
elif st.session_state.page == "prediction":

    if st.button("⬅ Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.title("🔍 Credit Risk Prediction")

    col1, col2 = st.columns(2)

    with col1:
        debt = st.number_input("Debt Ratio", value=0.5)
        income = st.number_input("Monthly Income", value=5000.0)

    with col2:
        late = st.number_input("Late Payments (90 days)", value=0)
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
            st.success("🟢 Low Risk")
        elif prob < 0.6:
            st.warning("🟡 Medium Risk")
        else:
            st.error("🔴 High Risk")

        st.progress(float(prob))
        st.metric("Default Probability", f"{prob:.2f}")
