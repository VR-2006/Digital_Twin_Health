import pandas as pd
import joblib
import numpy as np

model = joblib.load('models/model.pkl')
scaler = joblib.load('models/scaler.pkl')

df = pd.read_csv('data/heart.csv')
df = pd.get_dummies(df, drop_first=True)

features = df.drop('target', axis=1).columns

def prepare_input(input_dict):
    input_df = pd.DataFrame([input_dict])
    input_df = pd.get_dummies(input_df)
    input_df = input_df.reindex(columns=features, fill_value=0)
    return scaler.transform(input_df)

patient = {
    'age': 55,
    'sex': 'Male',
    'chest_pain_type': 'Asymptomatic',
    'resting_blood_pressure': 150,
    'cholestoral': 280,
    'fasting_blood_sugar': 'Yes',
    'rest_ecg': 'ST-T Abnormality',
    'Max_heart_rate': 100,
    'exercise_induced_angina': 'Yes'
}

processed = prepare_input(patient)
risk = model.predict_proba(processed)[0][1]

print(f"\nPredicted Risk: {risk:.2f}")

importances = model.feature_importances_

importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

top_features = importance_df.head(5)

print("\nTop Features Used:")
print(top_features['Feature'].values)

def generate_local_explanation(patient, top_features):
    explanations = []

    for feature in top_features['Feature']:

        if "blood_pressure" in feature and patient['resting_blood_pressure'] > 140:
            explanations.append("High blood pressure is increasing risk")

        elif "cholestoral" in feature and patient['cholestoral'] > 250:
            explanations.append("High cholesterol contributes to artery blockage")

        elif "heart_rate" in feature and patient['Max_heart_rate'] < 110:
            explanations.append("Low heart rate response indicates poor cardiac fitness")

        elif "age" in feature and patient['age'] > 50:
            explanations.append("Age is a contributing risk factor")

        elif "angina" in feature and patient['exercise_induced_angina'] == "Yes":
            explanations.append("Exercise-induced angina indicates cardiac stress")

        if len(explanations) == 0:
           explanations.append("No strong abnormal indicators detected, but model identified subtle risk patterns")


    return explanations

print("\nExplanation:\n")

explanations = generate_local_explanation(patient, top_features)

for exp in explanations:
    print(f"- {exp}")