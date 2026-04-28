import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="Credit Risk Intelligence", page_icon="💳", layout="wide")

# ---------- SESSION ----------
if "user_name" not in st.session_state:
    st.session_state.user_name = None

# ---------- WELCOME PAGE ----------
if st.session_state.user_name is None:

    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, black 80%);
    }

    .main-container {
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        padding-top:120px;
    }

    .glass {
        background: rgba(255,255,255,0.05);
        padding:20px;
        border-radius:16px;
        backdrop-filter: blur(10px);
        border:1px solid rgba(255,255,255,0.08);
        text-align:center;
        margin-bottom:20px;
    }

    .title {
        font-size:44px;
        font-weight:800;
        color:white;
        text-shadow: 0 0 10px rgba(0,255,255,0.6),
                     0 0 20px rgba(0,255,255,0.3);
        white-space: nowrap;
    }

    .subtitle {
        color:#aaa;
        font-size:15px;
        margin-top:8px;
    }

    .stTextInput>div>div>input {
        text-align:center;
        border-radius:10px;
        width:220px !important;
        margin:auto;
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

    .stButton>button:hover {
        box-shadow: 0 0 12px rgba(0,198,255,0.8);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

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

    st.markdown("</div>", unsafe_allow_html=True)

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
page = st.sidebar.radio("", ["🏠 Home", "📊 Dashboard", "🔍 Prediction"])

if st.sidebar.button("Logout"):
    st.session_state.user_name = None
    st.rerun()

# ---------- HEADER ----------
st.markdown(f"### 💳 Credit Risk Intelligence")
st.markdown(f"👋 Hello, {st.session_state.user_name}")

# ---------- HOME ----------
if page == "🏠 Home":

    st.markdown("## 👋 Welcome")
    st.write("### Credit Risk Intelligence Platform")

    st.write("---")

    st.subheader("🚀 What this app does")
    st.write("""
    - Predicts loan default risk using Machine Learning  
    - Uses XGBoost model for high accuracy  
    - Provides real-time risk classification  
    - Gives financial insights based on inputs  
    """)

    st.subheader("📊 Key Inputs")
    st.write("""
    - Debt Ratio  
    - Monthly Income  
    - Late Payments  
    - Credit Utilization  
    """)

# ---------- DASHBOARD ----------
elif page == "📊 Dashboard":
    st.title("📊 Dashboard (Coming next)")

# ---------- PREDICTION (UNCHANGED) ----------
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

        # 🔒 SAME LOGIC
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
st.markdown("Made with ❤️ using Machine Learning & Streamlit")
