import pandas as pd
import joblib
import numpy as np

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
    
    # Add rule-based logic
    if input_dict['resting_blood_pressure'] > 140:
        risk += 0.05
    if input_dict['cholestoral'] > 250:
        risk += 0.05
    
    return min(risk, 1.0)

base_patient = {
    'age': 40,
    'sex': 'Male',
    'chest_pain_type': 'Non-anginal Pain',
    'resting_blood_pressure': 120,
    'cholestoral': 200,
    'fasting_blood_sugar': 'No',
    'rest_ecg': 'Normal',
    'Max_heart_rate': 150,
    'exercise_induced_angina': 'No'
}

risk = calculate_risk(base_patient)
print("Base Risk:", risk)

bp_range = range(90, 180, 10)
risks = []

for bp in bp_range:
    temp = base_patient.copy()
    temp['resting_blood_pressure'] = bp
    
    r = calculate_risk(temp)
    risks.append(r)

print("\nSimulation Results:")
for bp, r in zip(bp_range, risks):
    print(f"BP: {bp} → Risk: {r:.2f}")