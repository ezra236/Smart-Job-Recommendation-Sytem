import pandas as pd
import numpy as np
from scipy.stats import mode
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer

# Load the CSV file
df = pd.read_csv('job110.csv')  # Replace with your actual file path

# Convert 'Job Salary' to numeric values
df['Job Salary'] = pd.to_numeric(df['Job Salary'], errors='coerce')

# One-Hot Encoding for 'Industry'
industry_dummies = pd.get_dummies(df['Industry'], prefix='Industry')

# One-Hot Encoding for 'Role Category' and 'Functional Area'
role_category_dummies = pd.get_dummies(df['Role Category'], prefix='Role_Category')
functional_area_dummies = pd.get_dummies(df['Functional Area'], prefix='Functional_Area')

# TF-IDF for 'Skills List'
vectorizer = TfidfVectorizer(stop_words='english')
skills_tfidf = vectorizer.fit_transform(df['Skills List'])

# Convert the TF-IDF matrix to a DataFrame
skills_df = pd.DataFrame(skills_tfidf.toarray(), columns=vectorizer.get_feature_names_out())

# Concatenate the original DataFrame with the new features
df_preprocessed = pd.concat([
    df, 
    industry_dummies, 
    skills_df, 
    role_category_dummies, 
    functional_area_dummies
], axis=1)

# Drop original columns that have been encoded
df_preprocessed = df_preprocessed.drop(['Industry', 'Skills List', 'Role Category', 'Functional Area'], axis=1)

# Ensure 'Job Experience Required' is in float format
df_preprocessed['Job Experience Required'] = df_preprocessed['Job Experience Required'].astype(float)

# Encode 'Job Title' (target) as integers
label_encoder = LabelEncoder()
df_preprocessed['Job Title'] = label_encoder.fit_transform(df_preprocessed['Job Title'])

# Separate features and target
X = df_preprocessed.drop(['Job Title'], axis=1)  # Features
y = df_preprocessed['Job Title']                  # Target

# Use SimpleImputer to fill missing values with the mean (if any)
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X_imputed, y, test_size=0.2, random_state=42
)

# Initialize the individual models with a fixed random_state for reproducibility
svm_model = LinearSVC(random_state=42)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
dt_model = DecisionTreeClassifier(random_state=42)

# Train each model on the training set
svm_model.fit(X_train, y_train)
rf_model.fit(X_train, y_train)
dt_model.fit(X_train, y_train)

# You can combine the three models into a VotingClassifier
ensemble_model = VotingClassifier(
    estimators=[('svm', svm_model), ('rf', rf_model), ('dt', dt_model)],
    voting='hard'  # Hard voting takes the majority vote
)
ensemble_model.fit(X_train, y_train)

# Make predictions on the test set using the ensemble model
ensemble_preds = ensemble_model.predict(X_test)

# Convert numerical predictions back to job titles
predicted_titles = label_encoder.inverse_transform(ensemble_preds)


accuracy = accuracy_score(y_test, ensemble_preds)
print("Predicted Job Titles:", predicted_titles)
print(f"Ensemble Accuracy: {accuracy * 100:.2f}%")
