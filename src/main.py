import pandas as pd

# Load dataset
df = pd.read_csv('data/heart.csv')

print("Dataset Loaded Successfully")
print(df.head())