# main.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# Load dataset
df = pd.read_csv('data/Crop_recommendation.csv')

# Split features and label
X = df.drop('label', axis=1)
y = df['label']

# Encode the label
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save model and encoder
with open('model/crop_model.pkl', 'wb') as f:
    pickle.dump((model, le), f)

print("✅ Model trained and saved.")
