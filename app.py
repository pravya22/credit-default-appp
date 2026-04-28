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

# ---------- WELCOME SCREEN ----------
if st.session_state.user_name is None:

    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, black 80%);
    }

    .center-box {
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        height:80vh;
    }

    .glass {
        background: rgba(255,255,255,0.05);
        padding:40px;
        border-radius:20px;
        backdrop-filter: blur(12px);
        border:1px solid rgba(255,255,255,0.1);
        text-align:center;
        width:100%;
    }

    .title {
        font-size:42px;
        font-weight:800;
        color:white;
        text-shadow: 0 0 15px rgba(0,255,255,0.7),
                     0 0 30px rgba(0,255,255,0.4);
        white-space: nowrap;
        margin-bottom:10px;
    }

    .subtitle {
        color:#aaa;
        font-size:16px;
        margin-bottom:25px;
    }

    .stTextInput>div>div>input {
        text-align:center;
    }

    .stButton>button {
        width:150px;
        border-radius:10px;
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        color:white;
        border:none;
        padding:10px;
        display:block;
        margin:auto;
    }

    .stButton>button:hover {
        box-shadow: 0 0 12px rgba(0,198,255,0.8);
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="center-box">', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# ---------- DARK UI ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
}

[data-testid="stSidebar"] {
    background: #020617;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.markdown("## 📌 Navigation")
page = st.sidebar.radio("", ["🏠 Home", "📊 Dashboard", "🔍 Prediction", "ℹ️ About"])

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
    st.title(f"👋 Hello, {st.session_state.user_name}")
    st.markdown("### Welcome to your dashboard")

# ---------- DASHBOARD ----------
elif page == "📊 Dashboard":
    st.title("📊 Dashboard")

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

        # 🔒 UNTOUCHED LOGIC
        if probability < 0.3:
            st.success("Low Risk")
        elif probability < 0.6:
            st.warning("Medium Risk")
        else:
            st.error("High Risk")

        st.progress(float(probability))
        st.metric("Default Probability", f"{probability:.2f}")

# ---------- ABOUT ----------
elif page == "ℹ️ About":
    st.title("ℹ️ About")
    st.write("""
    This app predicts loan default risk using Machine Learning.

    Model: XGBoost  

    Inputs:
    - Debt Ratio  
    - Monthly Income  
    - Late Payments  
    - Credit Utilization  
    """)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("Made with ❤️ using Machine Learning & Streamlit")



       
