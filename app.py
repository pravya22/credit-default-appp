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

if "page" not in st.session_state:
    st.session_state.page = "home"

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

        name = st.text_input("", placeholder="Enter your name")

        if st.button("Enter"):
            if name.strip():
                st.session_state.user_name = name
                st.rerun()

    st.stop()

# ---------- GLOBAL POLISH CSS (ONLY ADDITIONS) ----------
st.markdown("""
<style>

/* BUTTON FIX (VISIBLE + PREMIUM) */
.stButton>button {
    border-radius:12px;
    background: linear-gradient(135deg, #00c6ff, #7c3aed);
    color:white;
    border:none;
    padding:10px 18px;
    font-weight:600;
    box-shadow:0 0 15px rgba(0,198,255,0.4);
}

.stButton>button:hover {
    transform:scale(1.05);
    box-shadow:0 0 25px rgba(0,198,255,0.8);
}

/* LABEL VISIBILITY FIX */
label {
    color:#ddd !important;
    font-weight:500;
}

/* RESULT GLOW */
.result-box {
    text-align:center;
    padding:25px;
    border-radius:20px;
    margin-top:20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border:1px solid rgba(255,255,255,0.1);
    box-shadow:0 0 25px rgba(0,198,255,0.2);
}

/* RISK COLORS */
.low {color:#22c55e; font-weight:700;}
.medium {color:#facc15; font-weight:700;}
.high {color:#ef4444; font-weight:700;}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
col1, col2 = st.columns([6,1])
with col1:
    st.markdown("### 💳 Credit Risk Intelligence")
with col2:
    if st.button("Logout"):
        st.session_state.user_name = None
        st.session_state.page = "home"
        st.rerun()

# ---------- HOME (UNCHANGED CONTENT + BUTTON ADD) ----------
if st.session_state.page == "home":

    st.markdown(f"# 👋 Welcome, {st.session_state.user_name}")
    st.write("AI-powered platform for credit risk prediction")

    st.markdown("### 🚀 What this app does")
    st.markdown("""
- Predicts loan default risk  
- Uses ML model  
- Real-time classification  
- Helps decision making  
""")

    st.markdown("### 🧠 How it works")
    st.markdown("""
1. Enter financial data  
2. Model analyzes  
3. Get prediction  
""")

    st.markdown("")

    if st.button("🚀 Start Prediction"):
        st.session_state.page = "prediction"
        st.rerun()

# ---------- PREDICTION (POLISHED ONLY) ----------
elif st.session_state.page == "prediction":

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

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

        probability = model.predict_proba(input_df)[0][1]

        # Risk classification
        if probability < 0.3:
            risk = "LOW RISK"
            cls = "low"
        elif probability < 0.6:
            risk = "MEDIUM RISK"
            cls = "medium"
        else:
            risk = "HIGH RISK"
            cls = "high"

        # RESULT UI (IMPROVED)
        st.markdown(f"""
        <div class="result-box">
            <h2 class="{cls}">{risk}</h2>
            <h1>{probability:.2f}</h1>
        </div>
        """, unsafe_allow_html=True)

        st.progress(float(probability))
