import streamlit as st
import pandas as pd
import sys
import os

# -------------------------------
# FIX IMPORT PATH
# -------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.predictor import calculate_risk


# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="PhysioTwin AI",
    layout="wide"
)


# -------------------------------
# CUSTOM CSS (NEW 🔥)
# -------------------------------
st.markdown("""
<style>
.big-title {
    font-size: 42px;
    font-weight: bold;
}

.sub-text {
    color: gray;
    font-size: 16px;
}

.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #111827;
    color: white;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
}

.section {
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------
# TITLE SECTION (UPDATED)
# -------------------------------
st.markdown('<div class="big-title">PhysioTwin AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Personalized Health Simulation System</div>', unsafe_allow_html=True)
st.write("Simulate how physiological changes affect cardiovascular risk.")


# -------------------------------
# SIDEBAR INPUTS
# -------------------------------
st.sidebar.header("Patient Inputs")
st.sidebar.markdown("### Adjust Parameters")

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
# RESULT SECTION (CARD STYLE 🔥)
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
# EXPLANATION SECTION (CARD)
# -------------------------------
st.markdown('<div class="section"></div>', unsafe_allow_html=True)
st.header("Clinical Explanation")

st.markdown('<div class="card">', unsafe_allow_html=True)

explanations = generate_explanation(input_data)

for exp in explanations:
    st.write(f"• {exp}")

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# MULTI GRAPH DASHBOARD (DAY 17 🔥)
# -------------------------------
st.markdown('<div class="section"></div>', unsafe_allow_html=True)
st.header("Simulation Dashboard")

col1, col2, col3 = st.columns(3)

# -------------------------------
# BP GRAPH
# -------------------------------
with col1:
    st.subheader("Blood Pressure")

    bp_range = range(90, 180, 5)
    bp_risks = []

    for val in bp_range:
        temp = input_data.copy()
        temp['resting_blood_pressure'] = val
        bp_risks.append(calculate_risk(temp))

    bp_df = pd.DataFrame({
        "BP": list(bp_range),
        "Risk": bp_risks
    }).set_index("BP")

    st.line_chart(bp_df)


# -------------------------------
# CHOLESTEROL GRAPH
# -------------------------------
with col2:
    st.subheader("Cholesterol")

    chol_range = range(150, 350, 10)
    chol_risks = []

    for val in chol_range:
        temp = input_data.copy()
        temp['cholestoral'] = val
        chol_risks.append(calculate_risk(temp))

    chol_df = pd.DataFrame({
        "Cholesterol": list(chol_range),
        "Risk": chol_risks
    }).set_index("Cholesterol")

    st.line_chart(chol_df)


# -------------------------------
# HEART RATE GRAPH
# -------------------------------
with col3:
    st.subheader("Heart Rate")

    hr_range = range(60, 200, 5)
    hr_risks = []

    for val in hr_range:
        temp = input_data.copy()
        temp['Max_heart_rate'] = val
        hr_risks.append(calculate_risk(temp))

    hr_df = pd.DataFrame({
        "Heart Rate": list(hr_range),
        "Risk": hr_risks
    }).set_index("Heart Rate")

    st.line_chart(hr_df)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.warning("This system is for educational purposes only and not a medical diagnosis tool.")