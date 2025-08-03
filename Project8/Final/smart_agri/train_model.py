import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# Load dataset
df = pd.read_csv('data/Crop_recommendation.csv')

# Separate features and target
X = df.drop('label', axis=1)
y = df['label']

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Create model directory if it doesn't exist
os.makedirs('model', exist_ok=True)

# Save model and label encoder
with open('model/crop_model.pkl', 'wb') as f:
    pickle.dump({'model': model, 'le': le}, f)

print("✅ Model and LabelEncoder saved to model/crop_model.pkl")
