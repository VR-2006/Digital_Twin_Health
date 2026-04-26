import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

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
    if input_dict['Max_heart_rate'] < 100:
        risk += 0.05

    return min(risk, 1.0)

patient = {
    'age': 45,
    'sex': 'Male',
    'chest_pain_type': 'Non-anginal Pain',
    'resting_blood_pressure': 140,
    'cholestoral': 260,
    'fasting_blood_sugar': 'No',
    'rest_ecg': 'Normal',
    'Max_heart_rate': 120,
    'exercise_induced_angina': 'No'
}

days = 30
risk_over_time = []


for day in range(days):

    # Gradual improvement
    patient['resting_blood_pressure'] -= 0.5
    patient['cholestoral'] -= 0.7
    patient['Max_heart_rate'] += 0.3

    risk = calculate_risk(patient)
    risk_over_time.append(risk)

plt.figure()
plt.plot(range(days), risk_over_time)
plt.xlabel("Days")
plt.ylabel("Risk")
plt.title("Risk Over Time (Improving Health)")
plt.show()

patient2 = {
    'age': 45,
    'sex': 'Male',
    'chest_pain_type': 'Non-anginal Pain',
    'resting_blood_pressure': 120,
    'cholestoral': 200,
    'fasting_blood_sugar': 'No',
    'rest_ecg': 'Normal',
    'Max_heart_rate': 150,
    'exercise_induced_angina': 'No'
}

risk_worsening = []

for day in range(days):

    patient2['resting_blood_pressure'] += 0.7
    patient2['cholestoral'] += 0.8
    patient2['Max_heart_rate'] -= 0.4

    risk = calculate_risk(patient2)
    risk_worsening.append(risk)

plt.figure()
plt.plot(range(days), risk_over_time, label="Improving")
plt.plot(range(days), risk_worsening, label="Worsening")

plt.xlabel("Days")
plt.ylabel("Risk")
plt.title("Risk Evolution Over Time")

plt.legend()
plt.show()