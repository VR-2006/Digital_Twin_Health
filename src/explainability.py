import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt

model = joblib.load('models/model.pkl')

df = pd.read_csv('data/heart.csv')
df = pd.get_dummies(df, drop_first=True)

features = df.drop('target', axis=1).columns

importances = model.feature_importances_

importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': importances
})

importance_df = importance_df.sort_values(by='Importance', ascending=False)

print("Top Influencing Features:\n")

for i in range(5):
    print(f"{importance_df.iloc[i]['Feature']} → {importance_df.iloc[i]['Importance']:.3f}")

top5 = importance_df.head(5)

plt.figure()
plt.barh(top5['Feature'], top5['Importance'])
plt.xlabel("Importance")
plt.title("Top 5 Important Features")
plt.gca().invert_yaxis()
plt.show()

def clean_name(name):
    return name.replace("_", " ").title()
