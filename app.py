import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Page config
st.set_page_config(page_title="Credit Risk Predictor", page_icon="💳", layout="centered")

# Title
st.title("💳 Credit Default Prediction")
st.markdown("### AI-powered risk analysis using key financial indicators")

st.write("---")

# Sidebar
st.sidebar.header("📌 About")
st.sidebar.write("""
This app predicts loan default risk using Machine Learning.

Model: XGBoost  
Inputs:
- Debt Ratio  
- Monthly Income  
- Late Payments  
- Credit Utilization  
""")

# INPUTS
st.subheader("📥 Enter Customer Details")

col1, col2 = st.columns(2)

with col1:
    debt = st.number_input("Debt Ratio", min_value=0.0, value=0.5)
    income = st.number_input("Monthly Income", min_value=0.0, value=5000.0)

with col2:
    late = st.number_input("Late Payments (90 days)", min_value=0, value=0)
    util = st.number_input("Credit Utilization", min_value=0.0, value=0.3)

# Create input dataframe
input_df = pd.DataFrame([{
    "DebtRatio": debt,
    "MonthlyIncome": income,
    "NumberOfTimes90DaysLate": late,
    "RevolvingUtilizationOfUnsecuredLines": util
}])

st.write("---")

# PREDICTION
if st.button("🔍 Predict Risk"):

    probability = model.predict_proba(input_df)[0][1]

    st.subheader("📊 Prediction Result")

    # ✅ UPDATED THRESHOLDS (balanced)
    if probability < 0.3:
        st.success("✅ Low Risk")
    elif probability < 0.6:
        st.warning("⚠️ Medium Risk")
    else:
        st.error("🚨 High Risk")

    # Risk meter
    st.write("### Risk Score")
    st.progress(float(probability))

    # Show probability
    st.metric("Default Probability", f"{probability:.2f}")

    st.write("---")

    # EXPLANATION
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

    st.write("---")

# Footer
st.markdown("Made with ❤️ using Machine Learning & Streamlit")
