from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os
from dotenv import load_dotenv
import blockchain  # Contains the store_prediction function

# Load environment variables from .env file
load_dotenv()
account = os.getenv("ETH_ACCOUNT")
private_key = os.getenv("ETH_PRIVATE_KEY")
if not account or not private_key:
    raise Exception("Environment variables ETH_ACCOUNT and ETH_PRIVATE_KEY must be set.")

app = Flask(__name__)

# Load trained model and preprocessing artifacts
rf_model = joblib.load("rf_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")
label_encoder = joblib.load("label_encoder.pkl")
training_columns = joblib.load("training_columns.pkl")  # Load saved training columns

@app.route('/')
def home():
    return "Welcome to the Job Match Prediction API!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        # Expected keys: "Job Salary", "Job Experience Required", "Skills List", "Industry", "Role Category", "Functional Area"
        df_input = pd.DataFrame([data])
        
        # Preprocessing: Convert types
        df_input['Job Salary'] = pd.to_numeric(df_input['Job Salary'], errors='coerce')
        df_input['Job Experience Required'] = df_input['Job Experience Required'].astype(float)
        
        # Process 'Skills List' with TF-IDF
        skills_tfidf = vectorizer.transform(df_input['Skills List'])
        skills_df = pd.DataFrame(skills_tfidf.toarray(), columns=vectorizer.get_feature_names_out())
        
        # One-Hot Encoding for categorical features
        industry_dummies = pd.get_dummies(df_input['Industry'], prefix='Industry')
        role_category_dummies = pd.get_dummies(df_input['Role Category'], prefix='Role_Category')
        functional_area_dummies = pd.get_dummies(df_input['Functional Area'], prefix='Functional_Area')
        
        # Concatenate preprocessed features and reindex to match training features
        df_processed = pd.concat([
            df_input.drop(['Skills List', 'Industry', 'Role Category', 'Functional Area'], axis=1, errors='ignore'),
            industry_dummies, skills_df, role_category_dummies, functional_area_dummies
        ], axis=1)
        df_processed = df_processed.reindex(columns=training_columns, fill_value=0)
        
        # Make prediction
        prediction_numeric = rf_model.predict(df_processed)[0]
        predicted_title = label_encoder.inverse_transform([prediction_numeric])[0]
        reasoning = "Prediction based on skills similarity, salary range, and experience level."
        
        # Store on-chain by passing the account from environment variables
        tx_receipt = blockchain.store_prediction(predicted_title, reasoning, account)
        
        return jsonify({
            "predicted_title": predicted_title,
            "reasoning": reasoning,
            "transaction_hash": tx_receipt.transactionHash.hex()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
