import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
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

# Convert skills matrix to a DataFrame
skills_df = pd.DataFrame(skills_tfidf.toarray(), columns=vectorizer.get_feature_names_out())

# Concatenate the original dataframe with the one-hot encoded and TF-IDF features
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

# Encode 'Job Title' as integers using LabelEncoder
label_encoder = LabelEncoder()
df_preprocessed['Job Title'] = label_encoder.fit_transform(df_preprocessed['Job Title'])

X = df_preprocessed.drop(['Job Title'], axis=1)  # Features
y = df_preprocessed['Job Title']                  # Target


# Here we use SimpleImputer to fill missing values with the mean for each column.
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(
    X_imputed, y, test_size=0.2, random_state=42
)

# Using a linear SVM (LinearSVC) which is well-suited for high-dimensional sparse data
svm_model = LinearSVC(random_state=42)
svm_model.fit(X_train, y_train)

y_pred = svm_model.predict(X_test)

# Convert numerical predictions back to job titles
predicted_titles = label_encoder.inverse_transform(y_pred)

# Print the predicted job titles for the test set
print("Predicted Job Titles:", predicted_titles)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

