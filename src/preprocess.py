import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('data/heart.csv')

df = pd.get_dummies(df, drop_first=True)

print("\nAfter Encoding:")
print(df.head())

print("Dataset Shape:", df.shape)
print(df.head())

print("\nData Info:")
print(df.info())

X = df.drop('target', axis=1)
y = df['target']

print("\nFeatures Shape:", X.shape)
print("Target Shape:", y.shape)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("\nTrain Shape:", X_train.shape)
print("Test Shape:", X_test.shape)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

print("\nScaling Done")