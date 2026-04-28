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
    .stApp { background-color: black; }

    .center-box {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        height: 100vh;
        padding-top: 100px;
        color: white;
        text-align: center;
    }

    /* Glow Title */
    .title {
        font-size: 56px;
        font-weight: 800;
        color: white;
        text-shadow: 0 0 10px rgba(0,255,255,0.7),
                     0 0 20px rgba(0,255,255,0.5),
                     0 0 30px rgba(0,255,255,0.3);
        margin-bottom: 10px;
    }

    /* Typing Subtitle */
    .subtitle {
        color: #aaa;
        font-size: 18px;
        border-right: 2px solid #aaa;
        white-space: nowrap;
        overflow: hidden;
        width: 0;
        animation: typing 3s steps(30, end) forwards, blink 0.7s infinite;
        margin-bottom: 15px;
    }

    @keyframes typing {
        from { width: 0 }
        to { width: 320px }
    }

    @keyframes blink {
        50% { border-color: transparent }
    }

    /* Input box centered */
    div[data-baseweb="input"] {
        width: 300px;
        margin: auto;
        border-radius: 12px !important;
    }

    /* Button */
    .stButton>button {
        border-radius: 12px;
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
        margin-top: 10px;
    }

    .stButton>button:hover {
        box-shadow: 0 0 15px rgba(0, 198, 255, 0.8);
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

    # Title + subtitle
    st.markdown("""
    <div class="center-box">
        <div class="title">💳 Credit Risk Intelligence</div>
        <div class="subtitle">Welcome to AI-powered risk analysis</div>
    </div>
    """, unsafe_allow_html=True)

    # 👇 INPUT EXACTLY BELOW TITLE
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)

    name = st.text_input(
        "",
        placeholder="Enter your name"
    )

    if st.button("Enter"):
        if name.strip() != "":
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
.card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
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
    st.title("Dashboard")

# ---------- PREDICTION ----------
elif page == "🔍 Prediction":

    st.title("Credit Risk Prediction")

    col1, col2 = st.columns(2)

    with col1:
        debt = st.number_input("Debt Ratio", min_value=0.0, value=0.5)
        income = st.number_input("Monthly Income", min_value=0.0, value=5000.0)

    with col2:
        late = st.number_input("Late Payments", min_value=0, value=0)
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

# ---------- ABOUT ----------
elif page == "ℹ️ About":
    st.title("About")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("Made with ❤️ using Machine Learning & Streamlit")
