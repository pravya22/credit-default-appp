import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Page config
st.set_page_config(page_title="Credit Risk Dashboard", page_icon="💳", layout="wide")

# ---------- DARK THEME ----------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}
.stApp {
    background: linear-gradient(135deg, #0E1117, #111827);
}
h1, h2, h3, h4 {
    color: #FFFFFF;
}
.sidebar .sidebar-content {
    background-color: #111827;
}
.stButton>button {
    background-color: #2563EB;
    color: white;
    border-radius: 10px;
    padding: 10px;
}
.stButton>button:hover {
    background-color: #1D4ED8;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "",
    ["🏠 Home", "📊 Dashboard", "🔍 Prediction", "ℹ️ About"]
)

# ---------- HOME ----------
if page == "🏠 Home":
    st.title("💳 Credit Risk Intelligence")
    st.markdown("### AI-powered loan default prediction system")

    st.write("---")

    st.subheader("🚀 What this app does")
    st.markdown("""
    - Predicts loan default risk  
    - Uses Machine Learning (XGBoost)  
    - Provides real-time results  
    - Gives financial insights  
    """)

# ---------- DASHBOARD ----------
elif page == "📊 Dashboard":
    st.title("📊 Dashboard Overview")

    st.write("### Key Risk Indicators")

    col1, col2, col3 = st.columns(3)

    col1.metric("Model Accuracy", "85%")
    col2.metric("Avg Default Risk", "0.42")
    col3.metric("Model Type", "XGBoost")

    st.write("---")
    st.info("This dashboard gives a quick overview of the model performance.")

# ---------- PREDICTION ----------
elif page == "🔍 Prediction":

    st.title("🔍 Credit Risk Prediction")

    st.subheader("📥 Enter Customer Details")

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

    st.write("---")

    if st.button("🔍 Predict Risk"):

        probability = model.predict_proba(input_df)[0][1]

        st.subheader("📊 Prediction Result")

        # ✅ SAME LOGIC (UNCHANGED)
        if probability < 0.3:
            st.success("✅ Low Risk")
        elif probability < 0.6:
            st.warning("⚠️ Medium Risk")
        else:
            st.error("🚨 High Risk")

        st.write("### Risk Score")
        st.progress(float(probability))

        st.metric("Default Probability", f"{probability:.2f}")

        st.write("---")

        # Explanation (UNCHANGED)
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

# ---------- ABOUT ----------
elif page == "ℹ️ About":
    st.title("ℹ️ About This Project")

    st.markdown("""
    This application predicts whether a customer is likely to default on a loan.

    ### 🧠 Model Used
    - XGBoost Classifier

    ### 📥 Features Used
    - Debt Ratio  
    - Monthly Income  
    - Late Payments  
    - Credit Utilization  

    ### 🎯 Goal
    Help financial institutions assess credit risk quickly and accurately.
    """)

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("Made with ❤️ using Machine Learning & Streamlit")
