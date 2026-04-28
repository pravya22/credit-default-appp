import streamlit as st
import pandas as pd
import pickle

# Load model
model = pickle.load(open("model.pkl", "rb"))

# Page config
st.set_page_config(page_title="Credit Risk Intelligence", page_icon="💳", layout="wide")

# ---------- SESSION ----------
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# ---------- DARK UI ----------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at center, #0f172a 0%, black 80%);
}

/* Title */
.title {
    font-size: 48px;
    font-weight: 800;
    text-align: center;
    text-shadow: 0 0 15px rgba(0,255,255,0.6);
    white-space: nowrap;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #aaa;
    margin-bottom: 20px;
}

/* Button */
.stButton>button {
    border-radius: 10px;
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    color: white;
    padding: 10px 20px;
    display: block;
    margin: auto;
}
</style>
""", unsafe_allow_html=True)

# ---------- WELCOME PAGE ----------
if st.session_state.user_name == "":

    # spacing (instead of height:100vh)
    st.write("")
    st.write("")
    st.write("")

    st.markdown('<div class="title">💳 Credit Risk Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Welcome to AI-powered risk analysis</div>', unsafe_allow_html=True)

    # centered input
    col1, col2, col3 = st.columns([2,3,2])
    with col2:
        name = st.text_input("", placeholder="Enter your name")

    # centered button
    col1, col2, col3 = st.columns([3,2,3])
    with col2:
        if st.button("Enter"):
            if name.strip() != "":
                st.session_state.user_name = name
                st.rerun()

# ---------- MAIN APP ----------
else:

    # Sidebar
    st.sidebar.markdown("## 📌 Navigation")
    page = st.sidebar.radio("", ["🏠 Home", "📊 Dashboard", "🔍 Prediction"])

    if st.sidebar.button("Logout"):
        st.session_state.user_name = ""
        st.rerun()

    # ---------- HOME ----------
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

                <div style="display:flex; justify-content:space-between;">
                    <h2>💳 Credit Risk Intelligence</h2>
                    <span style="color:#aaa;">👋 {st.session_state.user_name}</span>
                </div>

                <hr style="border:0.5px solid rgba(255,255,255,0.1);">

                <div style="text-align:center;">
                    <h1>AI Credit Risk Prediction</h1>
                    <p style="color:#aaa;">
                        Smart loan default prediction using financial behavior analysis
                    </p>
                </div>

                <br>

                <div style="background: rgba(255,255,255,0.03); padding:20px; border-radius:12px;">
                    <h4>📌 What this app does</h4>
                    <p style="color:#bbb;">
                        Predicts whether a customer will default using ML based on financial inputs.
                    </p>
                </div>

                <br>

                <div style="display:flex; gap:15px;">
                    <div style="flex:1; background: rgba(255,255,255,0.03); padding:15px; border-radius:10px; text-align:center;">
                        🔍<br><b>Prediction</b>
                    </div>

                    <div style="flex:1; background: rgba(255,255,255,0.03); padding:15px; border-radius:10px; text-align:center;">
                        📊<br><b>Analysis</b>
                    </div>

                    <div style="flex:1; background: rgba(255,255,255,0.03); padding:15px; border-radius:10px; text-align:center;">
                        🧠<br><b>AI Model</b>
                    </div>
                </div>

                <br>

                <div style="color:#777; text-align:center;">
                    Made with ❤️ using Machine Learning
                </div>

            </div>
        </div>
        """, unsafe_allow_html=True)

    # ---------- DASHBOARD ----------
    elif page == "📊 Dashboard":
        st.title("📊 Dashboard")
        st.info("We’ll design this next.")

    # ---------- PREDICTION ----------
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
                st.success("✅ Low Risk")
            elif probability < 0.6:
                st.warning("⚠️ Medium Risk")
            else:
                st.error("🚨 High Risk")

            st.progress(float(probability))
            st.metric("Default Probability", f"{probability:.2f}")
       

       
