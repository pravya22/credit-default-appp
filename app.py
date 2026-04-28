import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.set_page_config(page_title="Credit Risk Intelligence", page_icon="💳", layout="wide")

# ---------- SESSION ----------
if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# ---------- GLOBAL CSS (ONLY FIXES) ----------
st.markdown("""
<style>
.stButton > button {
    background: linear-gradient(135deg, #00c6ff, #0072ff) !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 10px 18px !important;
    font-weight:600;
}

.stButton > button:hover {
    box-shadow: 0 0 10px rgba(0,198,255,0.6);
}

label {
    color: white !important;
    font-weight:600 !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 1️⃣ WELCOME PAGE (UNCHANGED)
# =========================================================
if st.session_state.page == "welcome":

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
    }
    </style>
    """, unsafe_allow_html=True)

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

# =========================================================
# 2️⃣ HOME PAGE (UNCHANGED DESIGN)
# =========================================================
elif st.session_state.page == "home":

    st.markdown(f"""
    <h1>👋 Welcome, {st.session_state.user_name}</h1>
    <p style="color:#aaa;">AI-powered platform for credit risk prediction</p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("📊 **Accurate Prediction**\n\nML powered insights")

    with col2:
        st.markdown("⚡ **Real-time Analysis**\n\nInstant results")

    with col3:
        st.markdown("📈 **Financial Insights**\n\nBetter decisions")

    st.markdown("---")

    st.markdown("## 🚀 What this app does")
    st.markdown("""
- Predicts loan default risk  
- Uses ML model  
- Real-time results  
- Helps decision making  
""")

    st.markdown("## 🧠 How it works")
    st.markdown("""
1. Enter details  
2. Model analyzes  
3. Get result  
""")

    # NAV BUTTONS
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🚀 Start Prediction"):
            st.session_state.page = "prediction"
            st.rerun()

    with col2:
        if st.button("Logout"):
            st.session_state.page = "welcome"
            st.rerun()

# =========================================================
# 3️⃣ PREDICTION PAGE (UNCHANGED)
# =========================================================
elif st.session_state.page == "prediction":

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
