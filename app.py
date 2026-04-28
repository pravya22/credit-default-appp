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

        c1, c2, c3 = st.columns([1,1.5,1])
        with c2:
            name = st.text_input("", placeholder="Enter your name")

        c4, c5, c6 = st.columns([1,1,1])
        with c5:
            if st.button("Enter"):
                if name.strip():
                    st.session_state.user_name = name
                    st.rerun()

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

.card {
    background: rgba(255,255,255,0.05);
    padding:20px;
    border-radius:15px;
    backdrop-filter: blur(10px);
    border:1px solid rgba(255,255,255,0.1);
    text-align:center;
    transition:0.3s;
}

.card:hover {
    box-shadow: 0 0 20px rgba(0,255,255,0.4);
}

.pill {
    display:inline-block;
    padding:8px 15px;
    margin:5px;
    border-radius:20px;
    background: rgba(0,255,255,0.1);
    border:1px solid rgba(0,255,255,0.3);
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
st.markdown(f"""
<div style="display:flex; justify-content:space-between; padding:10px;
background:rgba(255,255,255,0.05); border-radius:10px;">
<h3>💳 Credit Risk Intelligence</h3>
<p>👋 Hello, {st.session_state.user_name}</p>
</div>
""", unsafe_allow_html=True)

# ---------- HOME (UPDATED PREMIUM) ----------
if page == "🏠 Home":

    st.markdown(f"""
    <div style="text-align:center; margin-top:30px;">
        <h1>👋 Hello, {st.session_state.user_name}</h1>
        <p style="color:#aaa;">Welcome to Credit Risk Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("###")

    # Feature Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<div class='card'>📊<br><b>Predict Risk</b><br><small>Accurate loan default prediction</small></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='card'>⚡<br><b>Real-time Analysis</b><br><small>Instant risk classification</small></div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='card'>🧠<br><b>ML Powered</b><br><small>Powered by XGBoost model</small></div>", unsafe_allow_html=True)

    st.markdown("###")

    # Key Inputs
    st.markdown("<h3 style='text-align:center;'>📊 Key Inputs</h3>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;">
        <span class="pill">Debt Ratio</span>
        <span class="pill">Monthly Income</span>
        <span class="pill">Late Payments</span>
        <span class="pill">Credit Utilization</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("###")

    # CTA Button
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if st.button("🚀 Start Prediction"):
            st.session_state.page = "🔍 Prediction"
            st.rerun()

# ---------- DASHBOARD ----------
elif page == "📊 Dashboard":
    st.title("📊 Dashboard")

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
