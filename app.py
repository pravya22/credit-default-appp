import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Page config
st.set_page_config(page_title="Credit Risk Intelligence", page_icon="💳", layout="wide")

# ---------------- SESSION ----------------
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# ---------------- DARK UI ----------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0e1117;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- WELCOME PAGE ----------------
if st.session_state.user_name == "":

    st.markdown("""
    <div style='
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        height:80vh;
        text-align:center;
    '>
        <h1 style='font-size:42px;'>💳 Credit Risk Intelligence</h1>
        <p style='color:gray;'>Welcome to AI-powered risk analysis</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        name = st.text_input("", placeholder="Enter your name")

        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        if st.button("Enter"):
            if name.strip() != "":
                st.session_state.user_name = name
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- MAIN APP ----------------
else:

    # Sidebar
    st.sidebar.markdown("## 📌 Navigation")
    page = st.sidebar.radio("", ["🏠 Home", "📊 Dashboard", "🔍 Prediction"])

    if st.sidebar.button("Logout"):
        st.session_state.user_name = ""
        st.rerun()

    # ---------------- HOME ----------------
    if page == "🏠 Home":

        st.markdown(f"""
        <div style='display:flex; justify-content:center; margin-top:20px;'>

            <div style="
                width:900px;
                background: rgba(255,255,255,0.04);
                padding:40px;
                border-radius:18px;
                backdrop-filter: blur(10px);
                border:1px solid rgba(255,255,255,0.08);
            ">

                <!-- Header -->
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h2 style="margin:0;">💳 Credit Risk Intelligence</h2>
                    <span style="color:#aaa;">👋 {st.session_state.user_name}</span>
                </div>

                <hr style="border:0.5px solid rgba(255,255,255,0.1); margin:20px 0;">

                <!-- Hero -->
                <div style="text-align:center;">
                    <h1 style="margin-bottom:10px;">AI Credit Risk Prediction</h1>
                    <p style="color:#aaa; font-size:16px;">
                        Smart loan default prediction using financial behavior analysis
                    </p>
                </div>

                <br>

                <!-- What it does -->
                <div style="background: rgba(255,255,255,0.03); padding:20px; border-radius:12px;">
                    <h4>📌 What this app does</h4>
                    <p style="color:#bbb;">
                        This system predicts whether a customer is likely to default on a loan 
                        using machine learning. It analyzes financial indicators to provide 
                        fast and reliable risk insights.
                    </p>
                </div>

                <br>

                <!-- Features -->
                <div style="display:flex; gap:15px;">

                    <div style="flex:1; background: rgba(255,255,255,0.03); padding:15px; border-radius:10px; text-align:center;">
                        🔍<br><b>Instant Prediction</b><br>
                        <span style="color:#aaa; font-size:13px;">Real-time results</span>
                    </div>

                    <div style="flex:1; background: rgba(255,255,255,0.03); padding:15px; border-radius:10px; text-align:center;">
                        📊<br><b>Risk Analysis</b><br>
                        <span style="color:#aaa; font-size:13px;">Understand risk factors</span>
                    </div>

                    <div style="flex:1; background: rgba(255,255,255,0.03); padding:15px; border-radius:10px; text-align:center;">
                        🧠<br><b>ML Model</b><br>
                        <span style="color:#aaa; font-size:13px;">XGBoost powered</span>
                    </div>

                </div>

                <br>

                <!-- Inputs -->
                <div style="background: rgba(255,255,255,0.03); padding:20px; border-radius:12px;">
                    <h4>📥 Inputs Used</h4>
                    <ul style="color:#bbb;">
                        <li>Debt Ratio</li>
                        <li>Monthly Income</li>
                        <li>Late Payments</li>
                        <li>Credit Utilization</li>
                    </ul>
                </div>

                <br>

                <!-- Footer -->
                <div style="text-align:center; color:#777; font-size:13px;">
                    Made with ❤️ using Machine Learning & Streamlit
                </div>

            </div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- DASHBOARD (placeholder) ----------------
    elif page == "📊 Dashboard":
        st.title(f"📊 Dashboard")
        st.write(f"Hello, {st.session_state.user_name} 👋")
        st.info("Dashboard UI coming next...")

    # ---------------- PREDICTION (UNCHANGED LOGIC) ----------------
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
