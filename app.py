import streamlit as st
import pandas as pd
import pickle
import time

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Page config
st.set_page_config(page_title="Credit Risk Intelligence", page_icon="💳", layout="wide")

# ---------- SESSION STATE ----------
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# ---------- WELCOME SCREEN ----------
if st.session_state.user_name is None:

    st.markdown("""
    <style>
    .stApp { background-color: black; }
    .center-box {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 80vh;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="center-box">
        <h1 style="font-size:42px;">💳 Credit Risk Intelligence</h1>
        <p style="color:gray;">Welcome to AI-powered risk analysis</p>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input("Enter your name")

    if st.button("Enter"):
        if name.strip() != "":
            st.session_state.user_name = name
            st.rerun()

    st.stop()

# ---------- PREMIUM DARK UI ----------
st.markdown("""
<style>

/* Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid #1f2937;
}

/* Text */
h1, h2, h3, h4 {
    color: #f9fafb;
}
p, label {
    color: #d1d5db;
}

/* Glass Card */
.card {
    background: rgba(255, 255, 255, 0.05);
    padding: 30px;
    border-radius: 18px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 25px;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #3b82f6, #2563eb);
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    transition: all 0.2s ease-in-out;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 10px #3b82f6;
}

/* Input */
input, .stNumberInput input {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.markdown("## 📌 Navigation")
page = st.sidebar.radio(
    "",
    ["🏠 Home", "📊 Dashboard", "🔍 Prediction", "ℹ️ About"]
)

# Logout
if st.sidebar.button("🔓 Logout"):
    st.session_state.user_name = None
    st.rerun()

# ---------- HEADER ----------
st.markdown(f"""
<div style="
display:flex;
justify-content:space-between;
align-items:center;
padding:10px 20px;
background: rgba(255,255,255,0.05);
border-radius:10px;
margin-bottom:20px;
">
    <h3>💳 Credit Risk Intelligence</h3>
    <p>👋 Hello, {st.session_state.user_name}</p>
</div>
""", unsafe_allow_html=True)

# ---------- HOME ----------
if page == "🏠 Home":

    placeholder = st.empty()
    text = f"👋 Hello, {st.session_state.user_name}"
    typed = ""

    for char in text:
        typed += char
        placeholder.title(typed)
        time.sleep(0.02)

    st.markdown("### Welcome to your AI-powered dashboard")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🚀 What this app does")
    st.markdown("""
    - Predicts loan default risk  
    - Uses Machine Learning (XGBoost)  
    - Provides real-time results  
    - Gives financial insights  
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- DASHBOARD ----------
elif page == "📊 Dashboard":

    st.markdown("## 📊 Dashboard Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Model Accuracy", "85%")
    col2.metric("Avg Risk Score", "0.42")
    col3.metric("Model Type", "XGBoost")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.info("📊 Quick overview of model performance and risk insights.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- PREDICTION ----------
elif page == "🔍 Prediction":

    st.markdown("## 🔍 Credit Risk Prediction")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📥 Enter Customer Details")

    col1, col2 = st.columns(2)

    with col1:
        debt = st.number_input("Debt Ratio", min_value=0.0, value=0.5)
        income = st.number_input("Monthly Income", min_value=0.0, value=5000.0)

    with col2:
        late = st.number_input("Late Payments (90 days)", min_value=0, value=0)
        util = st.number_input("Credit Utilization", min_value=0.0, value=0.3)

    st.markdown('</div>', unsafe_allow_html=True)

    input_df = pd.DataFrame([{
        "DebtRatio": debt,
        "MonthlyIncome": income,
        "NumberOfTimes90DaysLate": late,
        "RevolvingUtilizationOfUnsecuredLines": util
    }])

    st.write("---")

    # ⚠️ PREDICTION LOGIC (UNCHANGED)
    if st.button("🔍 Predict Risk"):

        probability = model.predict_proba(input_df)[0][1]

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📊 Prediction Result")

        if probability < 0.3:
            st.success("✅ Low Risk")
        elif probability < 0.6:
            st.warning("⚠️ Medium Risk")
        else:
            st.error("🚨 High Risk")

        st.write("### Risk Score")
        st.progress(float(probability))

        st.metric("Default Probability", f"{probability:.2f}")
        st.caption("⚡ Powered by XGBoost Machine Learning Model")

        st.markdown('</div>', unsafe_allow_html=True)

        # EXPLANATION (UNCHANGED)
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("🧠 Why this prediction?")

        reasons = []

        if debt > 0.6:
            reasons.append("High Debt Ratio")
        if late > 2:
            reasons.append("Frequent Late Payments")
        if util > 0.7:
            reasons.append("High Credit Utilization")
        if income < 3000:
            reasons.append("Low Income")

        if reasons:
            for r in reasons:
                st.warning(f"⚠️ {r}")
        else:
            st.success("Financial profile looks stable")

        st.markdown('</div>', unsafe_allow_html=True)

# ---------- ABOUT ----------
elif page == "ℹ️ About":

    st.markdown("## ℹ️ About This Project")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown("""
    This application predicts loan default risk using Machine Learning.

    ### 🧠 Model
    - XGBoost Classifier  

    ### 📥 Features
    - Debt Ratio  
    - Monthly Income  
    - Late Payments  
    - Credit Utilization  

    ### 🎯 Goal
    Help financial institutions assess credit risk efficiently.
    """)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("Made with ❤️ using Machine Learning & Streamlit")
