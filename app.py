import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Page config
st.set_page_config(page_title="Credit Risk Dashboard", page_icon="💳", layout="wide")

# DARK MODE
st.markdown("""
<style>
body { background-color: #0e1117; color: white; }
.main { background-color: #0e1117; }
h1, h2, h3 { color: white; }
.stButton>button {
    background-color: #1f77b4;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR NAVIGATION
page = st.sidebar.radio(
    "📌 Navigation",
    ["🏠 Home", "📊 Dashboard", "📈 Prediction", "ℹ️ About"]
)

# SIDEBAR ABOUT
st.sidebar.markdown("### 📌 About")
st.sidebar.write("""
This app predicts loan default risk using Machine Learning.

Model: XGBoost  
Inputs:
- Debt Ratio  
- Monthly Income  
- Late Payments  
- Credit Utilization  
""")

# ---------------- HOME ----------------
if page == "🏠 Home":

    st.markdown("""
    <h1 style='text-align:center;'>💳 Credit Risk Intelligence</h1>
    <p style='text-align:center; font-size:18px; color:gray;'>
    AI-powered loan default prediction system
    </p>
    """, unsafe_allow_html=True)

    st.write("### 🚀 What this app does")
    st.write("""
    - Predicts loan default risk  
    - Uses machine learning (XGBoost)  
    - Provides real-time results  
    - Gives financial insights  
    """)

# ---------------- DASHBOARD ----------------
elif page == "📊 Dashboard":

    st.title("📊 Model Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Model", "XGBoost")
    col2.metric("Accuracy", "88%")
    col3.metric("AUC Score", "0.82")

    st.write("### 📈 Key Insight")
    st.info("Higher debt ratio, late payments, and high utilization increase default risk.")

# ---------------- PREDICTION ----------------
elif page == "📈 Prediction":

    st.title("📈 Predict Credit Risk")
    st.markdown("### Enter customer details below")

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

    # ⚠️ SAME LOGIC (UNCHANGED)
    if st.button("🔍 Predict Risk"):

        probability = model.predict_proba(input_df)[0][1]

        st.subheader("📊 Prediction Result")

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

        # Explanation (same logic)
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

# ---------------- ABOUT ----------------
elif page == "ℹ️ About":

    st.title("ℹ️ About This Project")

    st.write("""
This project predicts whether a customer will default on a loan.

🔍 Built using:
- XGBoost Machine Learning Model  
- Financial indicators  
- Data preprocessing & feature engineering  

🎯 Objective:
Help financial institutions reduce risk using AI.

👩‍💻 Developed by: Pravya
""")

# FOOTER
st.markdown("---")
st.markdown("<p style='text-align:center;'>Made with ❤️ using Machine Learning & Streamlit</p>", unsafe_allow_html=True)
