import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import joblib
import blockchain  # Import the blockchain.py module

# Load your CSV data (adjust the path if needed)
df = pd.read_csv('../data/combined_dataset.csv')

# Preprocess the data
df['Job Salary'] = pd.to_numeric(df['Job Salary'], errors='coerce')
industry_dummies = pd.get_dummies(df['Industry'], prefix='Industry')
role_category_dummies = pd.get_dummies(df['Role Category'], prefix='Role_Category')
functional_area_dummies = pd.get_dummies(df['Functional Area'], prefix='Functional_Area')

# TF-IDF vectorization for Skills List
vectorizer = TfidfVectorizer(stop_words='english')
skills_tfidf = vectorizer.fit_transform(df['Skills List'])
skills_df = pd.DataFrame(skills_tfidf.toarray(), columns=vectorizer.get_feature_names_out())

# Concatenate all features
df_preprocessed = pd.concat([df, industry_dummies, skills_df, role_category_dummies, functional_area_dummies], axis=1)
df_preprocessed = df_preprocessed.drop(['Industry', 'Skills List', 'Role Category', 'Functional Area'], axis=1)
df_preprocessed['Job Experience Required'] = df_preprocessed['Job Experience Required'].astype(float)

# Encode the target variable: Job Title
label_encoder = LabelEncoder()
df_preprocessed['Job Title'] = label_encoder.fit_transform(df_preprocessed['Job Title'])

# Split data into features and target
X = df_preprocessed.drop(['Job Title'], axis=1)
joblib.dump(list(X.columns), "training_columns.pkl")
y = df_preprocessed['Job Title']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

# Train the Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=60, random_state=42)
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy*100:.2f}%")

# For demonstration, pick the first prediction from the test set
predicted_numeric = y_pred[0]
predicted_title = label_encoder.inverse_transform([predicted_numeric])[0]

# Define a reasoning statement (in practice, this could include feature importance details)
reasoning = "Prediction based on skills similarity, salary range, and experience level."

# Save model and preprocessing artifacts for later use
joblib.dump(rf_model, "rf_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")
print("Model and preprocessing artifacts saved.")

# Store the predicted title and reasoning on-chain via the blockchain module
tx_receipt = blockchain.store_prediction(predicted_title, reasoning)
print("Stored prediction on-chain with transaction receipt:", tx_receipt)
