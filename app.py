import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("models/model.pkl", "rb"))

# Page config
st.set_page_config(page_title="Credit Risk Predictor", page_icon="💳", layout="centered")

# Title
st.title("💳 Credit Default Prediction")
st.markdown("### AI-powered risk analysis using key financial indicators")

st.write("---")

# Sidebar info
st.sidebar.header("📌 About")
st.sidebar.write("""
This app predicts whether a customer is likely to default on a loan.

Model: XGBoost  
Features used:
- Debt Ratio  
- Monthly Income  
- Late Payments  
- Credit Utilization  
""")

# ---- INPUT SECTION ----
st.subheader("📥 Enter Customer Details")

col1, col2 = st.columns(2)

with col1:
    debt = st.number_input("Debt Ratio", min_value=0.0, value=0.5)
    income = st.number_input("Monthly Income", min_value=0.0, value=5000.0)

with col2:
    late = st.number_input("Late Payments (90 days)", min_value=0, value=0)
    util = st.number_input("Credit Utilization", min_value=0.0, value=0.3)

# Create dataframe
input_df = pd.DataFrame([{
    "DebtRatio": debt,
    "MonthlyIncome": income,
    "NumberOfTimes90DaysLate": late,
    "RevolvingUtilizationOfUnsecuredLines": util
}])

st.write("---")

# ---- PREDICTION ----
if st.button("🔍 Predict Risk"):

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    st.subheader("📊 Prediction Result")

    # Show result
    if prediction == 1:
        st.error(f"⚠️ High Risk of Default")
    else:
        st.success(f"✅ Low Risk")

    st.metric(label="Default Probability", value=f"{probability:.2f}")

    st.write("---")

    # ---- SIMPLE EXPLANATION ----
    st.subheader("🧠 Key Risk Indicators")

    if debt > 0.6:
        st.warning("High Debt Ratio increases risk")

    if late > 2:
        st.warning("Frequent late payments detected")

    if util > 0.7:
        st.warning("High credit utilization")

    if income < 3000:
        st.warning("Low income may increase risk")

    if (debt <= 0.6 and late <= 2 and util <= 0.7 and income >= 3000):
        st.success("Financial profile looks stable")

    st.write("---")

# Footer
st.markdown("Made with ❤️ using Machine Learning & Streamlit")
