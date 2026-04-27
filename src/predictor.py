import pandas as pd
import joblib

# -------------------------------
# LOAD MODEL & SCALER
# -------------------------------
model = joblib.load('models/model.pkl')
scaler = joblib.load('models/scaler.pkl')

# -------------------------------
# LOAD DATA STRUCTURE
# -------------------------------
df = pd.read_csv('data/heart.csv')
df = pd.get_dummies(df, drop_first=True)

X_columns = df.drop('target', axis=1).columns


# -------------------------------
# FUNCTION: PREPARE INPUT
# -------------------------------
def prepare_input(input_dict):
    """
    Converts user input into model-ready format
    """

    input_df = pd.DataFrame([input_dict])

    # Convert categorical to numeric
    input_df = pd.get_dummies(input_df)

    # Match training columns
    input_df = input_df.reindex(columns=X_columns, fill_value=0)

    # Scale input
    input_scaled = scaler.transform(input_df)

    return input_scaled


# -------------------------------
# FUNCTION: CALCULATE RISK
# -------------------------------
def calculate_risk(input_dict):
    """
    Predicts risk using ML + rule-based adjustments
    """

    processed = prepare_input(input_dict)

    # ML prediction
    risk = model.predict_proba(processed)[0][1]

    # Rule-based adjustments
    if input_dict['resting_blood_pressure'] > 140:
        risk += 0.05

    if input_dict['cholestoral'] > 250:
        risk += 0.05

    if input_dict['Max_heart_rate'] < 100:
        risk += 0.05

    return min(risk, 1.0)

if __name__ == "__main__":
    sample = {
        'age': 45,
        'sex': 'Male',
        'chest_pain_type': 'Non-anginal Pain',
        'resting_blood_pressure': 130,
        'cholestoral': 220,
        'fasting_blood_sugar': 'No',
        'rest_ecg': 'Normal',
        'Max_heart_rate': 140,
        'exercise_induced_angina': 'No'
    }

    print("Risk:", calculate_risk(sample))