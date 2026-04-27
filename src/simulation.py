from predictor import calculate_risk

# -------------------------------
# BASE PATIENT DATA
# -------------------------------
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


# -------------------------------
# SINGLE RISK CHECK
# -------------------------------
risk = calculate_risk(base_patient)
print("Base Risk:", round(risk, 3))


# -------------------------------
# BP SIMULATION
# -------------------------------
bp_range = range(90, 180, 10)
risks = []

for bp in bp_range:
    simulated_patient = base_patient.copy()
    simulated_patient['resting_blood_pressure'] = bp

    risk_value = calculate_risk(simulated_patient)
    risks.append(risk_value)


# -------------------------------
# DISPLAY RESULTS
# -------------------------------
print("\nSimulation Results (BP vs Risk):")

for bp, r in zip(bp_range, risks):
    print(f"Blood Pressure: {bp} → Risk: {r:.2f}")