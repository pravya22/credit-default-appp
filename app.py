import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    import xgboost as xgb
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except Exception:
    XGBOOST_AVAILABLE = False

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

st.set_page_config(
    page_title="Credit Risk Prediction App",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Credit Risk Prediction using XGBoost + SHAP")
st.caption("Interactive demo app based on your project presentation.")  # topic from slides [file:1]

st.markdown("---")

st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Project Overview", "Upload Dataset & Train", "Manual Prediction", "Model Metrics"]
)

PRESENTATION_METRICS = pd.DataFrame({
    "Model": ["Logistic Regression", "Decision Tree", "XGBoost"],
    "Accuracy": [0.919509, 0.739784, 0.751732],
    "AUC": [0.696496, 0.632416, 0.783202]
})

FEATURE_COLUMNS = [
    "RevolvingUtilizationOfUnsecuredLines",
    "age",
    "NumberOfTime30-59DaysPastDueNotWorse",
    "DebtRatio",
    "MonthlyIncome",
    "NumberOfOpenCreditLinesAndLoans",
    "NumberOfTimes90DaysLate",
    "NumberRealEstateLoansOrLines",
    "NumberOfTime60-89DaysPastDueNotWorse",
    "NumberOfDependents"
]

TARGET_COLUMN = "SeriousDlqin2yrs"

@st.cache_data
def load_default_dataset(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df

def preprocess_data(df):
    df = df.copy()

    unnamed_cols = [col for col in df.columns if "unnamed" in col.lower()]
    if unnamed_cols:
        df = df.drop(columns=unnamed_cols)

    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not found in dataset.")

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    for col in FEATURE_COLUMNS:
        if col not in X.columns:
            X[col] = np.nan

    X = X[FEATURE_COLUMNS]

    imputer = SimpleImputer(strategy="median")
    X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=FEATURE_COLUMNS)

    return X_imputed, y, imputer

def train_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=5)
    }

    if XGBOOST_AVAILABLE:
        models["XGBoost"] = XGBClassifier(
            n_estimators=200,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            random_state=42
        )

    trained_models = {}
    results = []

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)[:, 1]
        else:
            y_prob = y_pred

        acc = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)

        trained_models[name] = model
        results.append({
            "Model": name,
            "Accuracy": round(acc, 6),
            "AUC": round(auc, 6)
        })

    results_df = pd.DataFrame(results).sort_values(by="AUC", ascending=False).reset_index(drop=True)
    return trained_models, results_df, X_train, X_test, y_train, y_test

def simple_risk_reasoning(input_df):
    row = input_df.iloc[0]
    reasons = []

    if row["RevolvingUtilizationOfUnsecuredLines"] > 0.7:
        reasons.append("High revolving utilization increases risk.")
    if row["NumberOfTimes90DaysLate"] > 0:
        reasons.append("History of 90+ days late payments increases risk.")
    if row["NumberOfTime30-59DaysPastDueNotWorse"] > 0:
        reasons.append("30–59 days past-due events increase risk.")
    if row["NumberOfTime60-89DaysPastDueNotWorse"] > 0:
        reasons.append("60–89 days past-due events increase risk.")
    if row["DebtRatio"] > 0.5:
        reasons.append("High debt ratio may signal repayment stress.")
    if row["MonthlyIncome"] < 3000:
        reasons.append("Lower monthly income may reduce repayment capacity.")
    if row["age"] < 25:
        reasons.append("Very young borrower profile may carry higher uncertainty.")
    if row["NumberOfDependents"] > 3:
        reasons.append("More dependents may increase financial burden.")

    if not reasons:
        reasons.append("Input profile shows relatively balanced risk indicators.")

    return reasons

def plot_feature_input(input_df):
    row = input_df.iloc[0]
    fig, ax = plt.subplots(figsize=(10, 4))
    numeric_vals = row.values.astype(float)
    ax.bar(FEATURE_COLUMNS, numeric_vals, color="#4F46E5")
    ax.set_title("Input Feature Snapshot")
    ax.set_xticklabels(FEATURE_COLUMNS, rotation=75, ha="right")
    st.pyplot(fig)

if page == "Project Overview":
    st.subheader("Project Summary")
    st.write("""
    This app demonstrates a credit risk prediction workflow inspired by your presentation:
    - Predict whether a customer may default on a loan
    - Compare multiple ML models
    - Use XGBoost as the final model when available
    - Provide simple explainability for predictions
    """)

    st.subheader("Presentation-based Model Snapshot")
    st.dataframe(PRESENTATION_METRICS, use_container_width=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(PRESENTATION_METRICS["Model"], PRESENTATION_METRICS["AUC"], color=["#60A5FA", "#34D399", "#FBBF24"])
    ax.set_title("AUC Comparison from Presentation")
    ax.set_ylabel("AUC")
    st.pyplot(fig)

    st.info("According to the presentation, XGBoost had the highest AUC and was chosen as the final model.")

elif page == "Upload Dataset & Train":
    st.subheader("Upload Dataset and Train Models")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            df = load_default_dataset(uploaded_file)
            st.write("### Dataset Preview")
            st.dataframe(df.head(), use_container_width=True)

            st.write("### Dataset Shape")
            st.write(df.shape)

            X, y, imputer = preprocess_data(df)

            st.write("### Processed Features")
            st.dataframe(X.head(), use_container_width=True)

            trained_models, results_df, X_train, X_test, y_train, y_test = train_models(X, y)

            st.session_state["trained_models"] = trained_models
            st.session_state["results_df"] = results_df
            st.session_state["imputer"] = imputer
            st.session_state["feature_columns"] = FEATURE_COLUMNS

            st.success("Models trained successfully.")

            st.write("### Model Results")
            st.dataframe(results_df, use_container_width=True)

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(results_df["Model"], results_df["AUC"], color="#22C55E")
            ax.set_title("Trained Model AUC Comparison")
            ax.set_ylabel("AUC")
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please upload the Give Me Some Credit dataset CSV to continue.")

elif page == "Manual Prediction":
    st.subheader("Manual Customer Risk Prediction")

    st.write("Enter borrower details below:")

    col1, col2 = st.columns(2)

    with col1:
        revolving = st.number_input("Revolving Utilization", min_value=0.0, value=0.30, step=0.01)
        age = st.number_input("Age", min_value=18, max_value=100, value=35)
        past_30_59 = st.number_input("30-59 Days Past Due Count", min_value=0, value=0)
        debt_ratio = st.number_input("Debt Ratio", min_value=0.0, value=0.40, step=0.01)
        monthly_income = st.number_input("Monthly Income", min_value=0.0, value=5000.0, step=100.0)

    with col2:
        open_lines = st.number_input("Open Credit Lines and Loans", min_value=0, value=5)
        late_90 = st.number_input("90 Days Late Count", min_value=0, value=0)
        real_estate_loans = st.number_input("Real Estate Loans or Lines", min_value=0, value=1)
        past_60_89 = st.number_input("60-89 Days Past Due Count", min_value=0, value=0)
        dependents = st.number_input("Number of Dependents", min_value=0, value=1)

    input_df = pd.DataFrame([{
        "RevolvingUtilizationOfUnsecuredLines": revolving,
        "age": age,
        "NumberOfTime30-59DaysPastDueNotWorse": past_30_59,
        "DebtRatio": debt_ratio,
        "MonthlyIncome": monthly_income,
        "NumberOfOpenCreditLinesAndLoans": open_lines,
        "NumberOfTimes90DaysLate": late_90,
        "NumberRealEstateLoansOrLines": real_estate_loans,
        "NumberOfTime60-89DaysPastDueNotWorse": past_60_89,
        "NumberOfDependents": dependents
    }])

    st.write("### Input Summary")
    st.dataframe(input_df, use_container_width=True)

    if st.button("Predict Risk"):
        if "trained_models" in st.session_state and "results_df" in st.session_state:
            results_df = st.session_state["results_df"]
            trained_models = st.session_state["trained_models"]
            best_model_name = results_df.iloc[0]["Model"]
            best_model = trained_models[best_model_name]

            pred = best_model.predict(input_df)[0]

            if hasattr(best_model, "predict_proba"):
                prob = best_model.predict_proba(input_df)[0][1]
            else:
                prob = float(pred)

            st.markdown("### Prediction Result")
            if pred == 1:
                st.error(f"High Risk of Default | Probability: {prob:.2%}")
            else:
                st.success(f"Low Risk of Default | Probability: {prob:.2%}")

            st.markdown("### Why this prediction?")
            reasons = simple_risk_reasoning(input_df)
            for r in reasons:
                st.write(f"- {r}")

            st.markdown("### Input Visualization")
            plot_feature_input(input_df)

        else:
            st.warning("Please train the models first from the 'Upload Dataset & Train' page.")

elif page == "Model Metrics":
    st.subheader("Model Performance")

    tab1, tab2 = st.tabs(["Presentation Metrics", "Trained Metrics"])

    with tab1:
        st.write("These values are taken from the presentation.")
        st.dataframe(PRESENTATION_METRICS, use_container_width=True)

        fig, ax = plt.subplots(figsize=(8, 4))
        x = np.arange(len(PRESENTATION_METRICS))
        width = 0.35

        ax.bar(x - width/2, PRESENTATION_METRICS["Accuracy"], width, label="Accuracy", color="#3B82F6")
        ax.bar(x + width/2, PRESENTATION_METRICS["AUC"], width, label="AUC", color="#10B981")

        ax.set_xticks(x)
        ax.set_xticklabels(PRESENTATION_METRICS["Model"], rotation=15)
        ax.set_title("Presentation Model Comparison")
        ax.legend()
        st.pyplot(fig)

    with tab2:
        if "results_df" in st.session_state:
            results_df = st.session_state["results_df"]
            st.dataframe(results_df, use_container_width=True)

            fig, ax = plt.subplots(figsize=(8, 4))
            x = np.arange(len(results_df))
            width = 0.35

            ax.bar(x - width/2, results_df["Accuracy"], width, label="Accuracy", color="#8B5CF6")
            ax.bar(x + width/2, results_df["AUC"], width, label="AUC", color="#F59E0B")

            ax.set_xticks(x)
            ax.set_xticklabels(results_df["Model"], rotation=15)
            ax.set_title("Trained Model Comparison")
            ax.legend()
            st.pyplot(fig)
        else:
            st.info("Train the models first to see live metrics.")
