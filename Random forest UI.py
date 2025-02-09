import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score


# Load the CSV file
df = pd.read_csv('job25.csv')  # Replace with your actual file path

# Convert 'Job Salary' to numeric values
df['Job Salary'] = pd.to_numeric(df['Job Salary'], errors='coerce')

# Step 2: One-Hot Encoding for 'Industry'
industry_dummies = pd.get_dummies(df['Industry'], prefix='Industry')

#One-Hot Encoding for 'Role Category' and 'Functional Area'
role_category_dummies = pd.get_dummies(df['Role Category'], prefix='Role_Category')
functional_area_dummies = pd.get_dummies(df['Functional Area'], prefix='Functional_Area')

# Step 3: TF-IDF for 'Skills List'
vectorizer = TfidfVectorizer(stop_words='english')
skills_tfidf = vectorizer.fit_transform(df['Skills List'])

# Convert skills matrix to a DataFrame
skills_df = pd.DataFrame(skills_tfidf.toarray(), columns=vectorizer.get_feature_names_out())

# Step 4: Concatenate the original dataframe with the one-hot encoded and TF-IDF features
df_preprocessed = pd.concat([df, industry_dummies, skills_df, role_category_dummies, functional_area_dummies], axis=1)

# Drop original columns
df_preprocessed = df_preprocessed.drop(['Industry', 'Skills List','Role Category', 'Functional Area'], axis=1)

# Ensure 'Job Experience Required' is in float format
df_preprocessed['Job Experience Required'] = df_preprocessed['Job Experience Required'].astype(float)

# Step 5: Encode 'Job Title' (target)
label_encoder = LabelEncoder()
df_preprocessed['Job Title'] = label_encoder.fit_transform(df_preprocessed['Job Title'])

# Step 6: Split data into features (X) and target (y)
X = df_preprocessed.drop(['Job Title'], axis=1)  # Features
y = df_preprocessed['Job Title']  # Target

# Step 8: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 9: Initialize and train the Random Forest Classifier model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Step 10: Make predictions
y_pred = rf_model.predict(X_test)

# Convert numerical predictions back to job titles
predicted_titles = label_encoder.inverse_transform(y_pred)

# Print the predicted job titles for the test set
print("Predicted Job Titles:", predicted_titles)

# Step 11: Evaluate the model's accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")    

# Compute metrics with zero_division=1 to handle undefined cases
precision = precision_score(y_test, y_pred, average='weighted', zero_division=1)
recall = recall_score(y_test, y_pred, average='weighted', zero_division=1)
f1 = f1_score(y_test, y_pred, average='weighted', zero_division=1)

# Print results
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall: {recall * 100:.2f}%")
print(f"F1 Score: {f1 * 100:.2f}%")




def predict_job_title():
    print("\nEnter details to predict the Job Title:")

    # Get user input
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
    skills_tfidf_vector = vectorizer.transform([skills_input])  # Convert skills to TF-IDF
    skills_features = skills_tfidf_vector.toarray()[0]  # Convert sparse matrix to array

    # Convert user input to DataFrame with correct column names
    user_input_df = pd.DataFrame([[
        job_salary, job_experience, *industry_features, *skills_features, *role_category_features, *functional_area_features
    ]], columns=X.columns)  # Ensure column names match

    # Make prediction
    predicted_label = rf_model.predict(user_input_df)
    predicted_job_title = label_encoder.inverse_transform(predicted_label)

    # Display result
    print("\nPredicted Job Title:", predicted_job_title[0])

# Call the function for user input
predict_job_title()
