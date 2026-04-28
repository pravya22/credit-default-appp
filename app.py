import streamlit as st
import pandas as pd
import pickle

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Credit Risk Intelligence",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
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

if "nav_page" not in st.session_state:
    st.session_state.nav_page = "Home"

# ---------------- WELCOME SCREEN ----------------
if st.session_state.user_name is None:

    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, black 80%);
    }

    .glass {
        background: rgba(255,255,255,0.05);
        padding: 30px;
        border-radius: 24px;
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255,255,255,0.10);
        text-align: center;
        margin-top: 90px;
    }

    .title {
        font-size: 42px;
        font-weight: 800;
        color: white;
        text-shadow: 0 0 15px rgba(0,255,255,0.7),
                     0 0 30px rgba(0,255,255,0.35);
        white-space: nowrap;
    }

    .subtitle {
        color: #b8c1cc;
        font-size: 15px;
        margin-top: 10px;
        margin-bottom: 20px;
    }

    .stTextInput>div>div>input {
        text-align: center;
        border-radius: 10px;
    }

    .stButton>button {
        width: 150px;
        border-radius: 12px;
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

    left, center, right = st.columns([1, 2, 1], gap="large")

    with center:
        st.markdown("""
        <div class="glass">
            <div class="title">💳 Credit Risk Intelligence</div>
            <div class="subtitle">Welcome to AI-powered risk analysis</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 2, 1], gap="medium")
        with c2:
            name = st.text_input("", placeholder="Enter your name")

        c4, c5, c6 = st.columns([1, 1, 1], gap="medium")
        with c5:
            if st.button("Enter"):
                if name.strip():
                    st.session_state.user_name = name.strip()
                    st.session_state.nav_page = "Home"
                    st.rerun()
                else:
                    st.warning("Please enter your name first.")

    st.stop()

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #020617, #000000 100%);
    color: white;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07111f 0%, #020617 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3, h4, h5, h6, p, label, li, div, span {
    color: white;
}

.hero {
    text-align: center;
    padding: 52px 34px;
    border-radius: 24px;
    background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.04));
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 14px;
}

.hero h1 {
    font-size: 44px;
    margin-bottom: 10px;
}

.hero p {
    color: #cbd5e1;
    font-size: 17px;
    max-width: 860px;
    margin: 0 auto;
}

.sidebar-brand {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 20px;
    text-align: center;
}

.sidebar-brand h2 {
    font-size: 22px;
    margin-bottom: 6px;
}

.sidebar-brand p {
    color: #cbd5e1;
    font-size: 13px;
}

.stats-strip {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    padding: 14px 18px;
    margin-bottom: 18px;
}

.stat-box {
    text-align: center;
    padding: 10px 6px;
}

.stat-box h3 {
    font-size: 24px;
    margin-bottom: 4px;
}

.stat-box p {
    color: #cbd5e1;
    font-size: 13px;
    margin: 0;
}

.metric-card {
    background: rgba(255,255,255,0.05);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    text-align: left;
    min-height: 155px;
}

.metric-card h3 {
    margin-bottom: 10px;
    font-size: 20px;
}

.metric-card p {
    color: #cbd5e1;
    font-size: 14px;
    line-height: 1.6;
}

.section-card {
    background: rgba(255,255,255,0.05);
    padding: 26px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    min-height: 245px;
}

.section-card h3 {
    margin-bottom: 14px;
    font-size: 22px;
}

.section-card p {
    color: #cbd5e1;
    line-height: 1.7;
}

.section-card ul,
.section-card ol {
    padding-left: 20px;
    color: #dbe4ee;
    line-height: 1.8;
}

.note-card {
    background: rgba(255,255,255,0.05);
    padding: 24px 28px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 8px;
}

.note-card p {
    color: #cbd5e1;
    line-height: 1.7;
}

.form-card {
    background: rgba(255,255,255,0.05);
    padding: 28px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 10px;
}

.result-box {
    text-align: center;
    padding: 25px;
    border-radius: 20px;
    margin-top: 20px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
}

.footer-box {
    text-align: center;
    padding-top: 24px;
    padding-bottom: 10px;
    color: #94a3b8;
    font-size: 13px;
}

.low { color: #22c55e; }
.medium { color: #facc15; }
.high { color: #ef4444; }

.small-muted {
    color: #94a3b8 !important;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h2>💳 Credit Risk</h2>
        <p>AI-powered loan default intelligence</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"**User:** {st.session_state.user_name}")
    st.markdown("")

    selected = st.radio(
        "Navigation",
        ["Home", "Prediction", "About"],
        index=["Home", "Prediction", "About"].index(st.session_state.nav_page)
    )
    st.session_state.nav_page = selected

    st.markdown("---")
    st.markdown("### App Highlights")
    st.markdown("- 4 financial input features")
    st.markdown("- Real-time risk prediction")
    st.markdown("- 3-level risk classification")
    st.markdown("- ML-based decision support")

    st.markdown("---")
    if st.button("Logout"):
        st.session_state.user_name = None
        st.session_state.nav_page = "Home"
        st.rerun()

# ---------------- TOP HEADER ----------------
st.markdown("## 💳 Credit Risk Intelligence")

# ---------------- HOME PAGE ----------------
if st.session_state.nav_page == "Home":

    st.markdown(f"""
    <div class="hero">
        <h1>👋 Welcome, {st.session_state.user_name}</h1>
        <p>Analyze applicant financial data, estimate default probability, and support smarter lending decisions with a clean enterprise-style credit risk workflow.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="stats-strip">', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3, gap="medium")
    with s1:
        st.markdown("""
        <div class="stat-box">
            <h3>4</h3>
            <p>Core input features</p>
        </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown("""
        <div class="stat-box">
            <h3>3</h3>
            <p>Risk levels generated</p>
        </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown("""
        <div class="stat-box">
            <h3>Real-time</h3>
            <p>Instant prediction workflow</p>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    r1c1, r1c2, r1c3 = st.columns(3, gap="medium")

    with r1c1:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Prediction Engine</h3>
            <p>Generates a probability-based risk estimate using key borrower financial attributes.</p>
        </div>
        """, unsafe_allow_html=True)

    with r1c2:
        st.markdown("""
        <div class="metric-card">
            <h3>⚡ Fast Review</h3>
            <p>Helps reduce initial screening effort by surfacing applicant risk quickly and consistently.</p>
        </div>
        """, unsafe_allow_html=True)

    with r1c3:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 Decision Support</h3>
            <p>Supports financial evaluation with structured output for low, medium, and high-risk profiles.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    r2c1, r2c2 = st.columns(2, gap="large")

    with r2c1:
        st.markdown("""
        <div class="section-card">
            <h3>🚀 What this app does</h3>
            <ul>
                <li>Predicts loan default risk</li>
                <li>Uses a trained machine learning model</li>
                <li>Returns a probability-based outcome</li>
                <li>Supports credit-review workflows</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with r2c2:
        st.markdown("""
        <div class="section-card">
            <h3>🧠 Workflow overview</h3>
            <ol>
                <li>Enter the applicant's financial details</li>
                <li>The model evaluates core risk signals</li>
                <li>A probability score is generated</li>
                <li>The profile is classified into a risk band</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    r3c1, r3c2 = st.columns(2, gap="large")

    with r3c1:
        st.markdown("""
        <div class="section-card">
            <h3>📌 Inputs used</h3>
            <ul>
                <li>Debt Ratio</li>
                <li>Monthly Income</li>
                <li>Late Payments</li>
                <li>Credit Utilization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with r3c2:
        st.markdown("""
        <div class="section-card">
            <h3>✅ Why it matters</h3>
            <ul>
                <li>Improves consistency in early review</li>
                <li>Highlights red-flag profiles sooner</li>
                <li>Supports faster screening decisions</li>
                <li>Brings structure to credit evaluation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class="note-card">
        <h3>⚠️ Important Note</h3>
        <p>This application is a decision-support tool. Final loan approval decisions should also consider internal policy, document verification, and human judgment.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    a1, a2, a3 = st.columns([2, 1, 2], gap="medium")
    with a2:
        if st.button("🚀 Go to Prediction"):
            st.session_state.nav_page = "Prediction"
            st.rerun()

    st.markdown("""
    <div class="footer-box">
        Built with Streamlit and machine learning for enterprise-style credit risk screening.
    </div>
    """, unsafe_allow_html=True)

# ---------------- PREDICTION PAGE ----------------
elif st.session_state.nav_page == "Prediction":

    st.markdown("""
    <div class="hero" style="padding:30px;">
        <h1>🔍 Credit Risk Prediction</h1>
        <p>Enter applicant financial details to estimate the probability of default and classify the risk profile.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown("### Applicant Details")
    st.caption("Use the fields below to run a real-time credit risk assessment.")

    p1, p2 = st.columns(2, gap="large")

    with p1:
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

    with p2:
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

    b1, b2, b3 = st.columns([1, 1, 4], gap="medium")
    with b1:
        predict_btn = st.button("Predict Risk")
    with b2:
        reset_btn = st.button("Reset Form")

    st.markdown('</div>', unsafe_allow_html=True)

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

    st.markdown("""
    <div class="footer-box">
        Prediction results should be reviewed alongside lending policy and verification checks.
    </div>
    """, unsafe_allow_html=True)

# ---------------- ABOUT PAGE ----------------
elif st.session_state.nav_page == "About":

    st.markdown("""
    <div class="hero" style="padding:32px;">
        <h1>ℹ️ About This Project</h1>
        <p>A Streamlit-based machine learning application designed to support loan default risk evaluation through simple, explainable financial input features.</p>
    </div>
    """, unsafe_allow_html=True)

    a1, a2 = st.columns(2, gap="large")

    with a1:
        st.markdown("""
        <div class="section-card">
            <h3>📘 Project Overview</h3>
            <p>This application estimates credit risk using four applicant-level financial features. It is designed as a lightweight decision-support tool for academic demonstration and practical screening workflows.</p>
        </div>
        """, unsafe_allow_html=True)

    with a2:
        st.markdown("""
        <div class="section-card">
            <h3>🧩 Core Features</h3>
            <ul>
                <li>Interactive Streamlit interface</li>
                <li>Machine learning based prediction</li>
                <li>Probability output with risk classification</li>
                <li>Simple financial input workflow</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    b1, b2 = st.columns(2, gap="large")

    with b1:
        st.markdown("""
        <div class="section-card">
            <h3>📌 Input Variables</h3>
            <ul>
                <li>Debt Ratio</li>
                <li>Monthly Income</li>
                <li>Late Payments</li>
                <li>Credit Utilization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with b2:
        st.markdown("""
        <div class="section-card">
            <h3>⚠️ Disclaimer</h3>
            <p>This tool should not be used as the sole basis for loan approval. It is intended to support analysis and demonstrate machine learning driven credit-risk assessment.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="footer-box">
        Built as a modern Streamlit machine learning project for credit risk intelligence.
    </div>
    """, unsafe_allow_html=True)
