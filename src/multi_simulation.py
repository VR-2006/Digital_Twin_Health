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

    # Rule adjustments
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

bp_values = range(100, 170, 10)
chol_values = range(180, 300, 20)
hr_values = range(90, 170, 20)

results = []

for bp in bp_values:
    for chol in chol_values:
        for hr in hr_values:

            temp = base_patient.copy()
            temp['resting_blood_pressure'] = bp
            temp['cholestoral'] = chol
            temp['Max_heart_rate'] = hr

            risk = calculate_risk(temp)

            results.append({
                'BP': bp,
                'Cholesterol': chol,
                'HeartRate': hr,
                'Risk': risk
            })
results_df = pd.DataFrame(results)
print(results_df.head())

bp_group = results_df.groupby('BP')['Risk'].mean()

plt.figure()
plt.plot(bp_group.index, bp_group.values)
plt.xlabel("Blood Pressure")
plt.ylabel("Average Risk")
plt.title("BP vs Risk (Multi-parameter)")
plt.show()

chol_group = results_df.groupby('Cholesterol')['Risk'].mean()

plt.figure()
plt.plot(chol_group.index, chol_group.values)
plt.xlabel("Cholesterol")
plt.ylabel("Average Risk")
plt.title("Cholesterol vs Risk")
plt.show()