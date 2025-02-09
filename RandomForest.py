import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score

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

