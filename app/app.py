import streamlit as st
import pandas as pd
import sys
import os

# -------------------------------
# FIX IMPORT PATH
# -------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# -------------------------------
# IMPORT MODEL LOGIC
# -------------------------------
from src.predictor import calculate_risk


# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="PhysioTwin AI", layout="wide")


# -------------------------------
# CSS
# -------------------------------
st.markdown("""
<style>
.big-title { font-size: 42px; font-weight: bold; }
.sub-text { color: gray; }
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #111827;
    color: white;
}
.section { margin-top: 30px; }
</style>
""", unsafe_allow_html=True)


# -------------------------------
# TITLE
# -------------------------------
st.markdown('<div class="big-title">PhysioTwin AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Personalized Health Simulation System</div>', unsafe_allow_html=True)
st.markdown("### 🔍 Real-time Health Simulation Dashboard")


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
# SCENARIO
# -------------------------------
scenario = st.selectbox(
    "Choose Lifestyle Scenario",
    ["Custom", "Healthy", "High Risk", "Sedentary", "Athlete"]
)


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
# APPLY SCENARIO
# -------------------------------
if scenario == "Healthy":
    input_data['resting_blood_pressure'] -= 15
    input_data['cholestoral'] -= 40
    input_data['Max_heart_rate'] += 20

elif scenario == "High Risk":
    input_data['resting_blood_pressure'] += 25
    input_data['cholestoral'] += 60
    input_data['Max_heart_rate'] -= 30

elif scenario == "Sedentary":
    input_data['resting_blood_pressure'] += 10
    input_data['cholestoral'] += 30
    input_data['Max_heart_rate'] -= 15

elif scenario == "Athlete":
    input_data['resting_blood_pressure'] -= 10
    input_data['cholestoral'] -= 20
    input_data['Max_heart_rate'] += 30


# -------------------------------
# CALCULATE RISK (DIRECT MODEL 🔥)
# -------------------------------
risk = calculate_risk(input_data)


# -------------------------------
# RESULT
# -------------------------------
st.markdown('<div class="section"></div>', unsafe_allow_html=True)
st.header("Risk Assessment")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.metric("Risk Probability", f"{risk*100:.2f}%")
    st.progress(int(risk * 100))
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if risk > 0.7:
        st.error("High Risk")
    elif risk > 0.4:
        st.warning("Moderate Risk")
    else:
        st.success("Low Risk")
    st.markdown('</div>', unsafe_allow_html=True)


# -------------------------------
# EXPLANATION
# -------------------------------
st.markdown('<div class="section"></div>', unsafe_allow_html=True)
st.header("Clinical Explanation")

if risk > 0.7:
    st.write("• High cardiovascular strain detected")
elif risk > 0.4:
    st.write("• Moderate lifestyle risk factors observed")
else:
    st.write("• Healthy cardiovascular condition")


# -------------------------------
# DASHBOARD
# -------------------------------
st.markdown('<div class="section"></div>', unsafe_allow_html=True)
st.header("Simulation Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    bp_range = range(90, 180, 5)
    st.line_chart(pd.DataFrame({
        "BP": list(bp_range),
        "Risk": [calculate_risk({**input_data, 'resting_blood_pressure': v}) for v in bp_range]
    }).set_index("BP"))

with col2:
    chol_range = range(150, 350, 10)
    st.line_chart(pd.DataFrame({
        "Chol": list(chol_range),
        "Risk": [calculate_risk({**input_data, 'cholestoral': v}) for v in chol_range]
    }).set_index("Chol"))

with col3:
    hr_range = range(60, 200, 5)
    st.line_chart(pd.DataFrame({
        "HR": list(hr_range),
        "Risk": [calculate_risk({**input_data, 'Max_heart_rate': v}) for v in hr_range]
    }).set_index("HR"))


# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.warning("This system is for educational purposes only.")