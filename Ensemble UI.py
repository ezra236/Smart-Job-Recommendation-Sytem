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

# Convert back to DataFrame with column names
X = pd.DataFrame(X_imputed, columns=X.columns)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
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


# Function to Predict Job Title
def predict_job_title():
    print("\nEnter details to predict the Job Title:")
    industry_input = input("Enter Industry: ")
    role_category_input = input("Enter Role Category: ")
    functional_area_input = input("Enter Functional Area: ")
    job_experience = float(input("Enter Job Experience Required (in years): "))
    job_salary = float(input("Enter Expected Job Salary: ").replace(",", ""))
    skills_input = input("Enter Skills (comma separated): ")

    # One-Hot Encoding for user input
    industry_features = [1 if col == f'Industry_{industry_input}' else 0 for col in industry_dummies.columns]
    role_category_features = [1 if col == f'Role_Category_{role_category_input}' else 0 for col in role_category_dummies.columns]
    functional_area_features = [1 if col == f'Functional_Area_{functional_area_input}' else 0 for col in functional_area_dummies.columns]
    
    # TF-IDF Vectorization for skills
    skills_tfidf_vector = vectorizer.transform([skills_input])
    skills_features = skills_tfidf_vector.toarray()[0]
    
    # Convert user input to DataFrame with correct column names
    user_input_df = pd.DataFrame([[
        job_salary, job_experience, *industry_features, *skills_features, *role_category_features, *functional_area_features
    ]], columns=X.columns)
    
    # Make prediction
    predicted_label = ensemble_model.predict(user_input_df)
    predicted_job_title = label_encoder.inverse_transform(predicted_label)
    
    print("\nPredicted Job Title:", predicted_job_title[0])

# Call function to predict job title
predict_job_title()
