import pandas as pd
from flask import Flask, render_template, request
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the trained model and preprocessing objects
df = pd.read_csv('job110.csv')  # Replace with your actual file path

# Convert 'Job Salary' to numeric values
df['Job Salary'] = pd.to_numeric(df['Job Salary'], errors='coerce')

# One-Hot Encoding for categorical features
industry_dummies = pd.get_dummies(df['Industry'], prefix='Industry')
role_category_dummies = pd.get_dummies(df['Role Category'], prefix='Role_Category')
functional_area_dummies = pd.get_dummies(df['Functional Area'], prefix='Functional_Area')

# TF-IDF for 'Skills List'
vectorizer = TfidfVectorizer(stop_words='english')
skills_tfidf = vectorizer.fit_transform(df['Skills List'])
skills_df = pd.DataFrame(skills_tfidf.toarray(), columns=vectorizer.get_feature_names_out())

# Preprocess dataset
df_preprocessed = pd.concat([df, industry_dummies, skills_df, role_category_dummies, functional_area_dummies], axis=1)
df_preprocessed.drop(['Industry', 'Skills List', 'Role Category', 'Functional Area'], axis=1, inplace=True)
df_preprocessed['Job Experience Required'] = df_preprocessed['Job Experience Required'].astype(float)

# Encode 'Job Title'
label_encoder = LabelEncoder()
df_preprocessed['Job Title'] = label_encoder.fit_transform(df_preprocessed['Job Title'])

# Prepare features and labels
X = df_preprocessed.drop(['Job Title'], axis=1)
y = df_preprocessed['Job Title']

# Train the model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X, y)

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    industry_input = request.form['industry']
    role_category_input = request.form['role_category']
    functional_area_input = request.form['functional_area']
    job_experience = float(request.form['job_experience'])
    job_salary = float(request.form['job_salary'].replace(",", ""))
    skills_input = request.form['skills']

    # One-Hot Encoding for user input
    industry_features = [1 if col == f'Industry_{industry_input}' else 0 for col in industry_dummies.columns]
    role_category_features = [1 if col == f'Role_Category_{role_category_input}' else 0 for col in role_category_dummies.columns]
    functional_area_features = [1 if col == f'Functional_Area_{functional_area_input}' else 0 for col in functional_area_dummies.columns]

    # TF-IDF for skills
    skills_tfidf_vector = vectorizer.transform([skills_input])
    skills_features = skills_tfidf_vector.toarray()[0]

    # Create DataFrame for input
    user_input_df = pd.DataFrame([[
        job_salary, job_experience, *industry_features, *skills_features, *role_category_features, *functional_area_features
    ]], columns=X.columns)

    # Predict
    predicted_label = rf_model.predict(user_input_df)
    predicted_job_title = label_encoder.inverse_transform(predicted_label)[0]

    return render_template('index.html', prediction=predicted_job_title)

if __name__ == '__main__':
    app.run(debug=True)
