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

# ---------- WELCOME SCREEN (LOCKED - DO NOT TOUCH) ----------
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

        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            name = st.text_input("", placeholder="Enter your name")

        c4, c5, c6 = st.columns([1,1,1])
        with c5:
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

/* INPUT LABEL FIX */
label {
    color: white !important;
    font-weight:600 !important;
}

/* RESULT BOX */
.result-box {
    padding: 28px;
    border-radius: 20px;
    text-align: center;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(12px);
    margin-top:20px;
    animation: fadeUp 0.5s ease-in-out;
}

@keyframes fadeUp {
    from {opacity:0; transform:translateY(15px);}
    to {opacity:1; transform:translateY(0);}
}

/* PROGRESS BAR */
.progress-container {
    height: 12px;
    width: 100%;
    background: #111;
    border-radius: 10px;
    margin-top:15px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    border-radius: 10px;
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

# ---------- HOME (UNCHANGED) ----------
if st.session_state.page == "home":

    st.markdown(f"""
    <div class="hero">
        <h1>👋 Welcome, {st.session_state.user_name}</h1>
        <p style="color:#bbb;">AI-powered platform for credit risk prediction</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Start Prediction"):
        st.session_state.page = "predict"
        st.rerun()

# ---------- PREDICTION ----------
elif st.session_state.page == "predict":

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
            risk = "🟢 LOW RISK"
            color = "#22c55e"
            insight = "Stable financial profile."
        elif prob < 0.6:
            risk = "🟡 MEDIUM RISK"
            color = "#f59e0b"
            insight = "Moderate financial risk."
        else:
            risk = "🔴 HIGH RISK"
            color = "#ef4444"
            insight = "High financial risk detected."

        st.markdown(f"""
        <div class="result-box" style="box-shadow:0 0 25px {color}40;">
            <h2 style="color:{color};">{risk}</h2>
            <p style="color:#aaa;">Default Probability</p>
            <h1>{prob:.2f}</h1>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="progress-container">
            <div class="progress-fill" style="
                width:{prob*100}%;
                background: linear-gradient(90deg, #00c6ff, {color});
            "></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 💡 Insight")
        st.info(insight)
