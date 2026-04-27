import pandas as pd
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
    if input_dict['Max_heart_rate'] < 100:
        risk += 0.05

    return min(risk, 1.0)

base_patient = {
    'age': 45,
    'sex': 'Male',
    'chest_pain_type': 'Non-anginal Pain',
    'resting_blood_pressure': 130,
    'cholestoral': 220,
    'fasting_blood_sugar': 'No',
    'rest_ecg': 'Normal',
    'Max_heart_rate': 130,
    'exercise_induced_angina': 'No'
}

def apply_scenario(patient, scenario):

    modified = patient.copy()

    if scenario == "healthy":
        modified['resting_blood_pressure'] -= 15
        modified['cholestoral'] -= 40
        modified['Max_heart_rate'] += 20

    elif scenario == "high_risk":
        modified['resting_blood_pressure'] += 25
        modified['cholestoral'] += 60
        modified['Max_heart_rate'] -= 30

    elif scenario == "sedentary":
        modified['resting_blood_pressure'] += 10
        modified['cholestoral'] += 30
        modified['Max_heart_rate'] -= 15

    elif scenario == "athlete":
        modified['resting_blood_pressure'] -= 10
        modified['cholestoral'] -= 20
        modified['Max_heart_rate'] += 30

    return modified

scenarios = ["healthy", "high_risk", "sedentary", "athlete"]

for s in scenarios:
    new_patient = apply_scenario(base_patient, s)
    risk = calculate_risk(new_patient)

    print(f"{s.upper()} → Risk: {risk:.2f}")