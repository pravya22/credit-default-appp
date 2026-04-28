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

        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            name = st.text_input("", placeholder="Enter your name")

        c4, c5, c6 = st.columns([1,1,1])
        with c5:
            if st.button("Enter"):
                if name.strip():
                    st.session_state.user_name = name
                    st.rerun()

    st.stop()

# ---------- GLOBAL UI ----------
st.markdown("""
<style>

/* REMOVE EXTRA SPACE */
header {visibility:hidden;}
.block-container {padding-top:1rem;}

/* BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #020617, #000000);
    color:white;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #000000);
    padding-top:30px;
}

/* NAV TITLE */
section[data-testid="stSidebar"] h2 {
    font-size:22px;
    font-weight:700;
    color:#00e5ff;
    text-align:center;
    letter-spacing:1px;
    text-shadow:
        0 0 10px rgba(0,229,255,0.9),
        0 0 25px rgba(0,229,255,0.6);
    margin-bottom:20px;
}

/* NAV ITEMS */
div[role="radiogroup"] > label {
    padding:14px;
    border-radius:14px;
    margin-bottom:12px;
    font-size:15px;
    color:#e5e7eb;
    transition:0.3s;
}

/* HOVER */
div[role="radiogroup"] > label:hover {
    background: rgba(0,229,255,0.12);
    transform: translateX(6px);
}

/* ACTIVE */
div[role="radiogroup"] input:checked + div {
    background: rgba(0,229,255,0.25);
    box-shadow:0 0 15px rgba(0,229,255,0.7);
    border-radius:12px;
    font-weight:600;
    color:white;
}

/* LOGOUT */
.stSidebar button {
    border-radius:12px;
    background: linear-gradient(135deg, #1f2937, #111827);
    color:white;
    border:1px solid rgba(255,255,255,0.1);
    margin-top:20px;
}

/* CARDS */
.card {
    background: rgba(255,255,255,0.05);
    padding:25px;
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.08);
    text-align:center;
    transition:0.3s;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow:0 0 20px rgba(0,229,255,0.3);
}

/* SECTION SPACING */
.section {
    margin-top:40px;
}

h1, h2, h3 {
    text-align:center;
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

# ---------- HOME ----------
if page == "🏠 Home":

    st.markdown(f"# 👋 Welcome, {st.session_state.user_name}")
    st.markdown("### Credit Risk Intelligence Platform")

    st.markdown('<div class="section"></div>', unsafe_allow_html=True)

    # WHAT APP DOES (IMPROVED)
    st.markdown("## 🚀 What this app does")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ✅ **Predicts loan default risk**  
        Using Machine Learning  
        
        ⚡ **Real-time analysis**  
        Instant classification  
        """)

    with col2:
        st.markdown("""
        🎯 **High accuracy model**  
        Powered by XGBoost  
        
        📊 **Financial insights**  
        Better decision making  
        """)

    st.markdown('<div class="section"></div>', unsafe_allow_html=True)

    # CARDS
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">📊<br><b>Accurate Prediction</b></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">⚡<br><b>Fast Results</b></div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">📈<br><b>Smart Insights</b></div>', unsafe_allow_html=True)

    st.markdown('<div class="section"></div>', unsafe_allow_html=True)

    # HOW IT WORKS (CLEAN)
    st.markdown("## 🧠 How it works")

    st.markdown("""
    **1.** Enter financial details  
    **2.** Model analyzes risk  
    **3.** Get instant prediction  
    """)

# ---------- DASHBOARD ----------
elif page == "📊 Dashboard":
    st.title("📊 Dashboard (Coming Soon)")

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
