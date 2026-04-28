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

# ---------- WELCOME PAGE (LOCKED - EXACT SAME) ----------
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

.stButton>button {
    background: linear-gradient(135deg, #00c6ff, #7c3aed);
    color:white;
    border:none;
    border-radius:10px;
    padding:10px 20px;
    font-weight:600;
}

label {
    color: #e5e7eb !important;
    font-size: 15px !important;
    font-weight: 600 !important;
}

.hero {
    text-align:center;
    padding:35px;
    border-radius:20px;
    background: rgba(255,255,255,0.05);
}

.card {
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:15px;
    text-align:center;
}

.info {
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:15px;
}

.section {margin-top:40px;}
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

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="card">📊<br><b>Accurate Prediction</b></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card">⚡<br><b>Real-time Analysis</b></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card">📈<br><b>Financial Insights</b></div>', unsafe_allow_html=True)

    st.markdown('<div class="section"></div>', unsafe_allow_html=True)

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
            label = "🟢 LOW RISK"
            color = "#22c55e"
        elif prob < 0.6:
            label = "🟡 MEDIUM RISK"
            color = "#f59e0b"
        else:
            label = "🔴 HIGH RISK"
            color = "#ef4444"

        # RESULT CARD
        st.markdown(f"""
        <div style="padding:25px;border-radius:18px;background:rgba(255,255,255,0.05);text-align:center;">
            <h2 style="color:{color};">{label}</h2>
            <h1>{prob:.2f}</h1>
        </div>
        """, unsafe_allow_html=True)

        st.progress(float(prob))

        # 📊 CHART
        st.subheader("📊 Input Overview")
        chart_df = pd.DataFrame({
            "Feature": ["Debt", "Income", "Late", "Utilization"],
            "Value": [debt, income/10000, late, util]
        })
        st.bar_chart(chart_df.set_index("Feature"))

        # 💡 EXPLANATION
        st.subheader("💡 Why this prediction?")
        reasons = []

        if debt > 0.6:
            reasons.append("High Debt Ratio increases risk")
        if late > 2:
            reasons.append("Frequent late payments detected")
        if util > 0.7:
            reasons.append("High credit utilization")

        if len(reasons) == 0:
            reasons.append("Your financial profile looks stable")

        for r in reasons:
            st.write("•", r)
