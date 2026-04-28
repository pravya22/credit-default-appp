import streamlit as st
import pandas as pd
import pickle

# ---------- LOAD ----------
model = pickle.load(open("model.pkl", "rb"))
data = pd.read_csv("your_dataset.csv")  # 🔁 change filename if needed

st.set_page_config(page_title="Credit Risk Intelligence", page_icon="💳", layout="wide")

# ---------- SESSION ----------
if "user_name" not in st.session_state:
    st.session_state.user_name = None

if "history" not in st.session_state:
    st.session_state.history = []

# ---------- WELCOME (UNCHANGED) ----------
if st.session_state.user_name is None:

    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at center, #0f172a 0%, black 80%);
    }
    .glass {
        background: rgba(255,255,255,0.05);
        padding:25px;
        border-radius:20px;
        backdrop-filter: blur(12px);
        border:1px solid rgba(255,255,255,0.1);
        text-align:center;
    }
    .title {
        font-size:40px;
        font-weight:800;
        color:white;
        text-shadow: 0 0 15px rgba(0,255,255,0.7),
                     0 0 30px rgba(0,255,255,0.4);
        white-space: nowrap;
    }
    .subtitle {
        color:#aaa;
        font-size:15px;
        margin-top:10px;
        margin-bottom:20px;
    }
    .stTextInput>div>div>input {
        text-align:center;
    }
    .stButton>button {
        width:140px;
        border-radius:10px;
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        color:white;
        border:none;
        padding:10px;
        display:block;
        margin:auto;
    }
    </style>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1,2,1])

    with center:
        st.markdown("""
        <div class="glass">
            <div class="title">💳 Credit Risk Intelligence</div>
            <div class="subtitle">Welcome to AI-powered risk analysis</div>
        </div>
        """, unsafe_allow_html=True)

        name = st.text_input("", placeholder="Enter your name")

        if st.button("Enter"):
            if name.strip():
                st.session_state.user_name = name
                st.rerun()

    st.stop()

# ---------- GLOBAL UI ----------
st.markdown("""
<style>
header {visibility:hidden;}
.block-container {padding-top:1rem;}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #020617, #000000 100%);
    color:white;
}
[data-testid="stSidebar"] {
    background: #020617;
    padding-top:30px;
}
section[data-testid="stSidebar"] h2 {
    color:#00c6ff;
    text-shadow:0 0 12px rgba(0,198,255,0.9);
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.markdown("## 🚀 Navigation")
page = st.sidebar.radio("", ["🏠 Home", "📊 Dashboard", "🔍 Prediction"])

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

# ---------- HOME (UNCHANGED) ----------
if page == "🏠 Home":
    st.markdown("## 👋 Welcome to Credit Risk Intelligence")

# ---------- DASHBOARD ----------
elif page == "📊 Dashboard":

    st.markdown("## 📊 Ultimate Credit Risk Dashboard")

    df = data.copy()
    hist_df = pd.DataFrame(st.session_state.history)

    df["RiskCategory"] = pd.cut(
        df["NumberOfTimes90DaysLate"],
        bins=[-1,1,3,100],
        labels=["Low","Medium","High"]
    )

    # FILTER
    risk_filter = st.selectbox("Filter Risk", ["All","Low","Medium","High"])
    if risk_filter != "All":
        df = df[df["RiskCategory"] == risk_filter]

    # KPI
    col1, col2, col3 = st.columns(3)
    col1.metric("Users", len(df))
    col2.metric("Avg Income", f"₹{int(df['MonthlyIncome'].mean())}")
    col3.metric("High Risk %", f"{(df['RiskCategory']=='High').mean()*100:.1f}%")

    st.markdown("---")

    # CHARTS
    c1, c2 = st.columns(2)

    with c1:
        st.bar_chart(df["RiskCategory"].value_counts())

    with c2:
        st.line_chart(df["MonthlyIncome"].head(100))

    st.markdown("---")

    st.scatter_chart(df[["DebtRatio","MonthlyIncome"]].head(200))

    st.markdown("---")

    st.dataframe(df.sort_values("NumberOfTimes90DaysLate", ascending=False).head(5))

    if not hist_df.empty:
        st.markdown("### 🔥 Live Predictions")
        st.dataframe(hist_df.tail(5))
        st.line_chart(hist_df["Risk"])

# ---------- PREDICTION (UNCHANGED + CONNECTED) ----------
elif page == "🔍 Prediction":

    st.title("🔍 Credit Risk Prediction")

    col1, col2 = st.columns(2)

    with col1:
        debt = st.number_input("Debt Ratio", value=0.5)
        income = st.number_input("Monthly Income", value=5000.0)

    with col2:
        late = st.number_input("Late Payments", value=0)
        util = st.number_input("Credit Utilization", value=0.3)

    input_df = pd.DataFrame([{
        "DebtRatio": debt,
        "MonthlyIncome": income,
        "NumberOfTimes90DaysLate": late,
        "RevolvingUtilizationOfUnsecuredLines": util
    }])

    if st.button("Predict Risk"):

        prob = model.predict_proba(input_df)[0][1]

        st.session_state.history.append({
            "DebtRatio": debt,
            "Income": income,
            "Late": late,
            "Utilization": util,
            "Risk": prob
        })

        if prob < 0.3:
            st.success("Low Risk")
        elif prob < 0.6:
            st.warning("Medium Risk")
        else:
            st.error("High Risk")

        st.metric("Probability", f"{prob:.2f}")
        st.progress(float(prob))

# ---------- FOOTER ----------
st.markdown("---")
