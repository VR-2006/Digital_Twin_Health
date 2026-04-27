import streamlit as st
import pandas as pd
import sys
import os

# -------------------------------
# FIX IMPORT PATH (IMPORTANT)
# -------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# -------------------------------
# IMPORT CORE LOGIC
# -------------------------------
from src.predictor import calculate_risk


# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="PhysioTwin AI",
    layout="wide"
)


# -------------------------------
# TITLE SECTION
# -------------------------------
st.title("PhysioTwin AI")
st.subheader("Personalized Health Risk Simulation System")
st.write("Simulate how physiological changes affect cardiovascular risk.")


# -------------------------------
# SIDEBAR INPUTS
# -------------------------------
st.sidebar.header("Patient Inputs")

age = st.sidebar.slider("Age", 20, 80, 40)
sex = st.sidebar.selectbox("Sex", ["Male", "Female"])
bp = st.sidebar.slider("Blood Pressure", 80, 200, 120)
chol = st.sidebar.slider("Cholesterol", 100, 400, 200)
hr = st.sidebar.slider("Max Heart Rate", 60, 200, 150)


# -------------------------------
# INPUT DATA
# -------------------------------
input_data = {
    'age': age,
    'sex': sex,
    'chest_pain_type': 'Non-anginal Pain',
    'resting_blood_pressure': bp,
    'cholestoral': chol,
    'fasting_blood_sugar': 'No',
    'rest_ecg': 'Normal',
    'Max_heart_rate': hr,
    'exercise_induced_angina': 'No'
}


# -------------------------------
# EXPLANATION FUNCTION
# -------------------------------
def generate_explanation(input_data):
    explanations = []

    if input_data['resting_blood_pressure'] > 140:
        explanations.append("High blood pressure increases cardiovascular strain")

    if input_data['cholestoral'] > 250:
        explanations.append("Elevated cholesterol contributes to artery blockage")

    if input_data['Max_heart_rate'] < 100:
        explanations.append("Lower heart rate response may indicate poor cardiac efficiency")

    if input_data['age'] > 55:
        explanations.append("Increased age is associated with higher cardiac risk")

    if len(explanations) == 0:
        explanations.append("All parameters are within healthy range")

    return explanations


# -------------------------------
# RISK CALCULATION
# -------------------------------
risk = calculate_risk(input_data)


# -------------------------------
# RESULT SECTION (IMPROVED UI)
# -------------------------------
st.markdown("---")
st.header("Risk Assessment")

col1, col2 = st.columns(2)

with col1:
    st.metric("Risk Probability", f"{risk*100:.2f}%")

with col2:
    if risk > 0.7:
        st.error("High Risk")
    elif risk > 0.4:
        st.warning("Moderate Risk")
    else:
        st.success("Low Risk")


# -------------------------------
# PROGRESS BAR (NEW 🔥)
# -------------------------------
st.progress(int(risk * 100))


# -------------------------------
# EXPLANATION SECTION
# -------------------------------
st.markdown("---")
st.header("Clinical Explanation")

explanations = generate_explanation(input_data)

for exp in explanations:
    st.markdown(f"- **{exp}**")


# -------------------------------
# GRAPH SECTION
# -------------------------------
st.markdown("---")
st.header("Simulation Graph (BP vs Risk)")

bp_range = range(90, 180, 5)
risks = []

for val in bp_range:
    temp = input_data.copy()
    temp['resting_blood_pressure'] = val
    risks.append(calculate_risk(temp))

graph_df = pd.DataFrame({
    "Blood Pressure": list(bp_range),
    "Risk": risks
}).set_index("Blood Pressure")

st.line_chart(graph_df)


# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.warning("This system is for educational purposes only and not a medical diagnosis tool.")