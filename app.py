import streamlit as st
import pandas as pd
import pickle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Credit Risk Intelligence",
    page_icon="💳",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# ---------------- SESSION ----------------
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------- WELCOME SCREEN ----------------
if st.session_state.user_name is None:

    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, black 80%);
    }

    .glass {
        background: rgba(255,255,255,0.05);
        padding: 25px;
        border-radius: 20px;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
        margin-top: 80px;
    }

    .title {
        font-size: 40px;
        font-weight: 800;
        color: white;
        text-shadow: 0 0 15px rgba(0,255,255,0.7),
                     0 0 30px rgba(0,255,255,0.4);
        white-space: nowrap;
    }

    .subtitle {
        color: #aaa;
        font-size: 15px;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    .stTextInput>div>div>input {
        text-align: center;
        border-radius: 10px;
    }

    .stButton>button {
        width: 140px;
        border-radius: 10px;
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        color: white;
        border: none;
        padding: 10px;
        display: block;
        margin: auto;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.markdown("""
        <div class="glass">
            <div class="title">💳 Credit Risk Intelligence</div>
            <div class="subtitle">Welcome to AI-powered risk analysis</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            name = st.text_input("", placeholder="Enter your name")

        c4, c5, c6 = st.columns([1, 1, 1])
        with c5:
            if st.button("Enter"):
                if name.strip():
                    st.session_state.user_name = name.strip()
                    st.session_state.page = "home"
                    st.rerun()
                else:
                    st.warning("Please enter your name first.")

    st.stop()

# ---------------- GLOBAL DARK UI ----------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #020617, #000000 100%);
    color: white;
}

/* Text */
h1, h2, h3, h4, h5, h6, p, label, li, div {
    color: white;
}

/* Header title spacing */
.block-container {
    padding-top: 2rem;
}

/* Hero */
.hero {
    text-align: center;
    padding: 35px;
    border-radius: 20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    text-align: center;
    min-height: 150px;
}

/* Info cards */
.info-card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    min-height: 230px;
}

/* Full width note */
.note-card {
    background: rgba(255,255,255,0.05);
    padding: 20px 25px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 15px;
}

/* Buttons */
.stButton>button {
    border-radius: 12px;
    background: linear-gradient(135deg, #00c6ff, #7c3aed);
    color: white;
    border: none;
    padding: 10px 18px;
    font-weight: 600;
}

/* Result box */
.result-box {
    text-align: center;
    padding: 25px;
    border-radius: 20px;
    margin-top: 20px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
}

/* Colors */
.low { color: #22c55e; }
.medium { color: #facc15; }
.high { color: #ef4444; }

/* Small muted text */
.muted {
    color: #cbd5e1 !important;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown("### 💳 Credit Risk Intelligence")
with col2:
    if st.button("Logout"):
        st.session_state.user_name = None
        st.session_state.page = "home"
        st.rerun()

# ---------------- HOME PAGE ----------------
if st.session_state.page == "home":

    st.markdown(f"""
    <div class="hero">
        <h1>👋 Welcome, {st.session_state.user_name}</h1>
        <p>Analyze applicant financial details, predict loan default probability, and support smarter credit decisions in real time.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
            <h3>📊 Accurate Prediction</h3>
            <p class="muted">Machine learning based risk classification using applicant financial data.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3>⚡ Real-Time Analysis</h3>
            <p class="muted">Instantly generate risk probability and classify the applicant profile.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <h3>📈 Better Financial Insights</h3>
            <p class="muted">Support loan screening decisions with fast and consistent model output.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="info-card">
            <h3>🚀 What this app does</h3>
            <ul>
                <li>Predicts loan default risk</li>
                <li>Uses a trained machine learning model</li>
                <li>Provides probability-based output</li>
                <li>Helps support credit evaluation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="info-card">
            <h3>🧠 How it works</h3>
            <ol>
                <li>Enter applicant financial details</li>
                <li>The model processes the input values</li>
                <li>Get a risk prediction instantly</li>
                <li>Review the result for decision support</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    c3, c4 = st.columns(2)

    with c3:
        st.markdown("""
        <div class="info-card">
            <h3>✨ Key Features</h3>
            <ul>
                <li>Instant loan default prediction</li>
                <li>Probability-based risk scoring</li>
                <li>Simple and user-friendly design</li>
                <li>Fast financial decision support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="info-card">
            <h3>📌 Inputs Used for Prediction</h3>
            <ul>
                <li>Debt Ratio</li>
                <li>Monthly Income</li>
                <li>Late Payments</li>
                <li>Credit Utilization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="note-card">
        <h3>⚠️ Important Note</h3>
        <p>This application provides AI-based credit risk insights for decision support. Final loan approval decisions should also include human judgment, policy rules, and additional verification.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    c5, c6, c7 = st.columns([2, 1, 2])
    with c6:
        if st.button("🚀 Start Prediction"):
            st.session_state.page = "prediction"
            st.rerun()

# ---------------- PREDICTION PAGE ----------------
elif st.session_state.page == "prediction":

    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("← Back"):
            st.session_state.page = "home"
            st.rerun()

    st.title("🔍 Credit Risk Prediction")
    st.caption("Enter the applicant's financial details below to estimate loan default risk.")

    col1, col2 = st.columns(2)

    with col1:
        debt = st.number_input(
            "Debt Ratio",
            min_value=0.0,
            max_value=10.0,
            value=0.50,
            step=0.01,
            format="%.2f",
            help="Debt ratio represents total debt relative to income."
        )

        income = st.number_input(
            "Monthly Income",
            min_value=0.0,
            value=5000.0,
            step=100.0,
            format="%.2f"
        )

    with col2:
        late = st.number_input(
            "Late Payments",
            min_value=0,
            max_value=50,
            value=0,
            step=1
        )

        util = st.number_input(
            "Credit Utilization",
            min_value=0.0,
            max_value=1.0,
            value=0.30,
            step=0.01,
            format="%.2f",
            help="Credit utilization is the proportion of used unsecured credit."
        )

    input_df = pd.DataFrame([{
        "DebtRatio": debt,
        "MonthlyIncome": income,
        "NumberOfTimes90DaysLate": late,
        "RevolvingUtilizationOfUnsecuredLines": util
    }])

    c3, c4, c5 = st.columns([1, 1, 4])

    with c3:
        predict_btn = st.button("Predict Risk")

    with c4:
        reset_btn = st.button("Reset")

    if reset_btn:
        st.rerun()

    if predict_btn:
        if income == 0:
            st.error("Monthly Income cannot be zero for meaningful credit analysis.")
        else:
            try:
                probability = float(model.predict_proba(input_df)[0][1])

                if probability < 0.30:
                    risk = "LOW RISK"
                    cls = "low"
                    msg = "Applicant appears financially stable based on the entered values."
                elif probability < 0.60:
                    risk = "MEDIUM RISK"
                    cls = "medium"
                    msg = "Applicant shows moderate risk. Additional review is recommended."
                else:
                    risk = "HIGH RISK"
                    cls = "high"
                    msg = "Applicant may have a strong chance of default. Proceed carefully."

                st.markdown(f"""
                <div class="result-box">
                    <h2 class="{cls}">{risk}</h2>
                    <h1>{probability * 100:.1f}%</h1>
                    <p>{msg}</p>
                </div>
                """, unsafe_allow_html=True)

                st.progress(probability)

                if probability < 0.30:
                    st.success("Prediction completed successfully.")
                elif probability < 0.60:
                    st.warning("Prediction completed: medium-risk profile detected.")
                else:
                    st.error("Prediction completed: high-risk profile detected.")

                st.subheader("Input Summary")
                st.dataframe(input_df, use_container_width=True, hide_index=True)

            except Exception:
                st.error("Prediction failed. Please check whether model.pkl matches these input features.")
