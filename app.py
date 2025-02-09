from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer

# Load the CSV file
df = pd.read_csv('job110.csv')

# Convert 'Job Salary' to numeric values
df['Job Salary'] = pd.to_numeric(df['Job Salary'], errors='coerce')

# One-Hot Encoding for 'Industry', 'Role Category', 'Functional Area'
industry_dummies = pd.get_dummies(df['Industry'], prefix='Industry')
role_category_dummies = pd.get_dummies(df['Role Category'], prefix='Role_Category')
functional_area_dummies = pd.get_dummies(df['Functional Area'], prefix='Functional_Area')

# TF-IDF for 'Skills List'
vectorizer = TfidfVectorizer(stop_words='english')
skills_tfidf = vectorizer.fit_transform(df['Skills List'])
skills_df = pd.DataFrame(skills_tfidf.toarray(), columns=vectorizer.get_feature_names_out())

# Preprocessing
df_preprocessed = pd.concat([df, industry_dummies, skills_df, role_category_dummies, functional_area_dummies], axis=1)
df_preprocessed = df_preprocessed.drop(['Industry', 'Skills List', 'Role Category', 'Functional Area'], axis=1)

# Encode target variable 'Job Title'
label_encoder = LabelEncoder()
df_preprocessed['Job Title'] = label_encoder.fit_transform(df_preprocessed['Job Title'])

# Features and Target
X = df_preprocessed.drop(['Job Title'], axis=1)
y = df_preprocessed['Job Title']

# Handle missing values
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)
X = pd.DataFrame(X_imputed, columns=X.columns)

# Train Models
svm_model = LinearSVC(random_state=42)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
dt_model = DecisionTreeClassifier(random_state=42)

# Train each model
svm_model.fit(X, y)
rf_model.fit(X, y)
dt_model.fit(X, y)

# Voting Ensemble
ensemble_model = VotingClassifier(
    estimators=[('svm', svm_model), ('rf', rf_model), ('dt', dt_model)],
    voting='hard'
)
ensemble_model.fit(X, y)

# Flask App
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        industry_input = request.form['industry']
        role_category_input = request.form['role_category']
        functional_area_input = request.form['functional_area']
        job_experience = float(request.form['experience'])
        job_salary = float(request.form['salary'].replace(",", ""))
        skills_input = request.form['skills']

        # One-Hot Encoding
        industry_features = [1 if col == f'Industry_{industry_input}' else 0 for col in industry_dummies.columns]
        role_category_features = [1 if col == f'Role_Category_{role_category_input}' else 0 for col in role_category_dummies.columns]
        functional_area_features = [1 if col == f'Functional_Area_{functional_area_input}' else 0 for col in functional_area_dummies.columns]

        # TF-IDF Vectorization
        skills_tfidf_vector = vectorizer.transform([skills_input])
        skills_features = skills_tfidf_vector.toarray()[0]

        # Format input for prediction
        user_input_df = pd.DataFrame([[
            job_salary, job_experience, *industry_features, *skills_features, *role_category_features, *functional_area_features
        ]], columns=X.columns)

        # Make prediction
        predicted_label = ensemble_model.predict(user_input_df)
        predicted_job_title = label_encoder.inverse_transform(predicted_label)

        return render_template("index.html", prediction=predicted_job_title[0])

    return render_template("index.html", prediction=None)

if __name__ == "__main__":
    app.run(debug=True)
