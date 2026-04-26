import streamlit as st
import pandas as pd
import numpy as np
import joblib

model = joblib.load('models/model.pkl')
scaler = joblib.load('models/scaler.pkl')

df = pd.read_csv('data/heart.csv')
df = pd.get_dummies(df, drop_first=True)
X_columns = df.drop('target', axis=1).columns

def prepare_input(input_dict):
    input_df = pd.DataFrame([input_dict])
    input_df = pd.get_dummies(input_df)
    input_df = input_df.reindex(columns=X_columns, fill_value=0)
    return scaler.transform(input_df)

def calculate_risk(input_dict):
    processed = prepare_input(input_dict)
    risk = model.predict_proba(processed)[0][1]

    if input_dict['resting_blood_pressure'] > 140:
        risk += 0.05
    if input_dict['cholestoral'] > 250:
        risk += 0.05

    return min(risk, 1.0) 

st.title("Personalized Digital Twin for Health Risk Simulation")
st.write("Simulate how physiological changes affect cardiovascular risk")

age = st.slider("Age", 20, 80, 40)

sex = st.selectbox("Sex", ["Male", "Female"])

bp = st.slider("Blood Pressure", 80, 200, 120)

chol = st.slider("Cholesterol", 100, 400, 200)

hr = st.slider("Max Heart Rate", 60, 200, 150)

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
if st.button("Simulate Risk"):

    risk = calculate_risk(input_data)

    st.markdown("---")
    st.header("Simulation Result")

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
    st.markdown("---")
    st.header("Clinical Explanation")

    explanations = generate_explanation(input_data, risk)

    for exp in explanations:
        st.write(f"- {exp}")
   
bp_range = range(90, 180, 5)
risks = []

for val in bp_range:
    temp = input_data.copy()
    temp['resting_blood_pressure'] = val
    risks.append(calculate_risk(temp))

st.line_chart(pd.DataFrame({
    "BP": list(bp_range),
    "Risk": risks
}).set_index("BP"))

def generate_explanation(input_data, risk):
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

st.title("PhysioTwin AI")
st.subheader("Personalized Health Risk Simulation")

st.markdown("---")
st.header("Patient Input")    
st.markdown("---")
st.header("Simulation Graph (BP vs Risk)")

bp_range = range(90, 180, 5)
risks = []

for val in bp_range:
        temp = input_data.copy()
        temp['resting_blood_pressure'] = val
        risks.append(calculate_risk(temp))

st.line_chart(pd.DataFrame({
        "Blood Pressure": list(bp_range),
        "Risk": risks
    }).set_index("Blood Pressure"))

st.markdown("---")
st.warning("This system is for educational purposes only and not a medical diagnosis tool.")


