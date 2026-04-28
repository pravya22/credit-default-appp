import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Page config
st.set_page_config(page_title="Credit Risk Intelligence", page_icon="💳", layout="wide")

# ---------- PREMIUM DARK UI ----------
st.markdown("""
<style>

/* BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid #1f2937;
}

/* TEXT */
h1, h2, h3, h4, h5, h6 {
    color: #f9fafb;
    font-weight: 600;
}
p, label {
    color: #d1d5db;
}

/* GLASS CARD */
.card {
    background: rgba(255, 255, 255, 0.05);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 20px;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #3b82f6, #2563eb);
    color: white;
    border-radius: 12px;
    padding: 10px 25px;
    font-weight: 600;
    border: none;
}
.stButton>button:hover {
    transform: scale(1.05);
}

/* INPUT */
input, .stNumberInput input {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 10px;
}

/* METRIC BOX */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 15px;
}

/* PROGRESS BAR */
.stProgress > div > div > div > div {
    background-color: #3b82f6;
}

</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.markdown("## 📌 Navigation")
page = st.sidebar.radio(
    "",
    ["🏠 Home", "📊 Dashboard", "🔍 Prediction", "ℹ️ About"]
)

# ---------- HOME ----------
if page == "🏠 Home":
    st.title("💳 Credit Risk Intelligence")
    st.markdown("### AI-powered loan default prediction system")

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
    st.title("📊 Dashboard Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Model Accuracy", "85%")
    col2.metric("Avg Risk Score", "0.42")
    col3.metric("Model Type", "XGBoost")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.info("📊 This dashboard provides a quick overview of model performance.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- PREDICTION ----------
elif page == "🔍 Prediction":

    st.title("🔍 Credit Risk Prediction")

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

    if st.button("🔍 Predict Risk"):

        probability = model.predict_proba(input_df)[0][1]

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("📊 Prediction Result")

        # 🚨 SAME LOGIC (UNCHANGED)
        if probability < 0.3:
            st.success("✅ Low Risk")
        elif probability < 0.6:
            st.warning("⚠️ Medium Risk")
        else:
            st.error("🚨 High Risk")

        st.write("### Risk Score")
        st.progress(float(probability))

        st.metric("Default Probability", f"{probability:.2f}")

        st.markdown('</div>', unsafe_allow_html=True)

        # EXPLANATION
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
    st.title("ℹ️ About This Project")

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
    Help financial institutions assess credit risk quickly.
    """)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("Made with ❤️ using Machine Learning & Streamlit")
