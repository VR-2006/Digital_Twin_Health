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

base_patient = {
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

bp_values = np.arange(100, 180, 5)
hr_values = np.arange(80, 180, 5)

risk_matrix = np.zeros((len(bp_values), len(hr_values)))

for i, bp in enumerate(bp_values):
    for j, hr in enumerate(hr_values):

        temp = base_patient.copy()
        temp['resting_blood_pressure'] = bp
        temp['Max_heart_rate'] = hr

        risk = calculate_risk(temp)
        risk_matrix[i, j] = risk

plt.figure()
plt.imshow(risk_matrix, aspect='auto')

plt.colorbar(label='Risk')

plt.xticks(range(len(hr_values)), hr_values, rotation=90)
plt.yticks(range(len(bp_values)), bp_values)

plt.xlabel("Heart Rate")
plt.ylabel("Blood Pressure")
plt.title("Risk Interaction: BP vs Heart Rate")

plt.show()