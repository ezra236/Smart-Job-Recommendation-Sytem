# predictor/views.py
import os
import pickle
import numpy as np
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from .models import Prediction  # Import the Prediction model

# Load your model objects as before
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'predictor', 'rf_model.pkl')
TFIDF_PATH = os.path.join(BASE_DIR, 'predictor', 'tfidf_vectorizer.pkl')
LABEL_ENCODER_PATH = os.path.join(BASE_DIR, 'predictor', 'label_encoder.pkl')
TRAINING_COLUMNS_PATH = os.path.join(BASE_DIR, 'predictor', 'training_columns.pkl')

rf_model = pickle.load(open(MODEL_PATH, 'rb'))
tfidf_vectorizer = pickle.load(open(TFIDF_PATH, 'rb'))
label_encoder = pickle.load(open(LABEL_ENCODER_PATH, 'rb'))
training_columns = pickle.load(open(TRAINING_COLUMNS_PATH, 'rb'))

def home(request):
    return render(request, 'Home.html')

def explore(request):
    prediction = None

    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        # Combine skills from all input fields into a single string
        skills = " ".join([request.POST.get(f'skill{i}', '') for i in range(1, 6)]).strip()
        years_experience = request.POST.get('years', 0)
        industry = request.POST.get('industry', '')
        role = request.POST.get('role', '')
        function_area = request.POST.get('function', '')

        try:
            years_experience = float(years_experience)
        except ValueError:
            years_experience = 0.0

        # Create a DataFrame with the raw input
        input_dict = {
            'Job Salary': [0],  # default value since it is not provided
            'Job Experience Required': [years_experience],
            'Industry': [industry],
            'Skills List': [skills],
            'Role Category': [role],
            'Functional Area': [function_area]
        }
        df_input = pd.DataFrame(input_dict)

        # One-Hot Encoding for categorical features
        industry_dummies = pd.get_dummies(df_input['Industry'], prefix='Industry')
        role_category_dummies = pd.get_dummies(df_input['Role Category'], prefix='Role_Category')
        functional_area_dummies = pd.get_dummies(df_input['Functional Area'], prefix='Functional_Area')

        # TF-IDF transformation for 'Skills List'
        skills_tfidf = tfidf_vectorizer.transform(df_input['Skills List'])
        skills_df = pd.DataFrame(skills_tfidf.toarray(), columns=tfidf_vectorizer.get_feature_names_out())

        # Concatenate all features and drop the original text columns
        df_transformed = pd.concat(
            [df_input, industry_dummies, skills_df, role_category_dummies, functional_area_dummies],
            axis=1
        )
        df_transformed = df_transformed.drop(['Industry', 'Skills List', 'Role Category', 'Functional Area'], axis=1)

        # Reindex to match training columns
        df_transformed = df_transformed.reindex(columns=training_columns, fill_value=0)

        # Make prediction
        prediction_encoded = rf_model.predict(df_transformed)
        prediction = label_encoder.inverse_transform(prediction_encoded)[0]

        # Save the username and predicted title to the database
        if username:  # Only save if username is provided
            Prediction.objects.create(username=username, predicted_title=prediction)

        # If this is an AJAX request, return JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'prediction': prediction})

    # For non-AJAX GET requests, render the template normally.
    return render(request, 'explore.html', {'prediction': prediction})





# predictor/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Ensure all fields are provided
        if username and email and password:
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
                # Redirect back to home instead of rendering Home.html here
                return redirect('home')
            try:
                # Create the user using Django's built-in create_user (which hashes the password)
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # Redirect to explore page after successful registration
                return redirect('explore')
            except Exception as e:
                messages.error(request, f"Error creating user: {e}")
                return redirect('home')
        else:
            messages.error(request, "All fields are required.")
            return redirect('home')
    
    # In case of a GET request, render the home page
    return render(request, 'Home.html')




# predictor/views.py
from django.shortcuts import render

def post(request):
    return render(request, 'post.html')




from django.http import JsonResponse
from django.shortcuts import render
from .models import Company

def create_company(request):
    if request.method == 'POST':
        company_name     = request.POST.get('company_name')
        company_location = request.POST.get('company_location')
        company_email    = request.POST.get('company_email')
        password         = request.POST.get('password')
        company_logo     = request.FILES.get('company_logo')  # Remember to handle file uploads

        # Create the Company record.
        Company.objects.create(
            company_name=company_name,
            company_location=company_location,
            company_email=company_email,
            password=password,  # For demo only; don't store plaintext!
            company_logo=company_logo
        )

        # If the request is AJAX, return a JSON response:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

        # Fallback: render the template (if not AJAX)
        return render(request, 'post.html', {'success_message': True})

    return render(request, 'post.html')



# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Company, JobDetail

def post_job(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        company_email = request.POST.get('company_email')
        skills_list = [request.POST.get(f'skill{i}', '').strip() for i in range(1, 6)]
        skills_list = [s for s in skills_list if s]
        skills = ", ".join(skills_list)

        try:
            company = Company.objects.get(company_email=company_email)
        except Company.DoesNotExist:
            # For AJAX, return an error in JSON:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({'error': "Company does not exist."}, status=400)
            return render(request, 'post.html', {'error': "Company does not exist."})

        JobDetail.objects.create(company=company, job_title=job_title, skills=skills)

        # If this is an AJAX request, return JSON with a notification flag.
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({'notification2': True})
        
        # Fallback: Render the page with the notification.
        return render(request, 'post.html', {'notification2': True})

    return render(request, 'post.html')




def job(request):
    return render(request, 'job.html')



def job(request):
    # Use select_related to fetch related company data in one query.
    job_details = JobDetail.objects.select_related('company').all()
    return render(request, 'job.html', {'job_details': job_details})


from django.shortcuts import render

def recommend_view(request):
    return render(request, 'recommend.html')


# predictor/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("Username:", username)   # Debug output
        print("Password:", password)   # Debug output

        user = authenticate(request, username=username, password=password)
        print("Authenticated user:", user)  # Should print a user object if authentication succeeded

        if user is not None:
            login(request, user)
            request.session['username'] = username  # Store username in session
            return redirect("recommend")
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "Home.html")
    else:
        return render(request, "Home.html")





from django.shortcuts import render
from django.db.models import Q
from .models import Prediction, JobDetail

def recommend_view(request):
    username = request.session.get('username')
    predicted_title = None
    job_matches = []

    if username:
        try:
            # Get the latest prediction for the logged-in user
            prediction_obj = Prediction.objects.filter(username=username).latest('created_at')
            predicted_title = prediction_obj.predicted_title
        except Prediction.DoesNotExist:
            predicted_title = None

    if predicted_title:
        # Build a Q query that matches any word from the predicted title
        words = predicted_title.split()
        query = Q()
        for word in words:
            query |= Q(job_title__icontains=word)
        job_matches = JobDetail.objects.filter(query)

    context = {
        'predicted_title': predicted_title,
        'job_matches': job_matches,
    }
    return render(request, 'recommend.html', context)





from django.shortcuts import render, redirect
from .models import Company

def company_signin(request):
    error_message = None
    if request.method == "POST":
        company_username = request.POST.get("company_username")
        company_password = request.POST.get("company_password")
        
        # Use filter() and then first() to get the first matching record
        company = Company.objects.filter(company_name=company_username, password=company_password).first()
        
        if not company:
            error_message = "Invalid company name or password"
            return render(request, "company_signin.html", {"error": error_message})
        
        # Store company info in session and redirect
        request.session["company_name"] = company.company_name
        return redirect("company")
    
    return render(request, "company_signin.html", {"error": error_message})



def company(request):
    company_name = request.session.get("company_name", "Unknown Company")
    return render(request, "company.html", {"company_name": company_name})



def company(request):
    company_name = request.session.get("company_name")
    job_list = []
    
    if company_name:
        # Use filter().first() to avoid MultipleObjectsReturned error
        company_obj = Company.objects.filter(company_name=company_name).first()
        if company_obj:
            job_list = JobDetail.objects.filter(company=company_obj)
        else:
            # Optionally handle the case where no company is found
            job_list = []
            
    context = {
        "company_name": company_name,
        "job_list": job_list,
    }
    return render(request, "company.html", context)




from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import JobDetail

@require_POST
def remove_job(request, job_id):
    try:
        job = JobDetail.objects.get(id=job_id)
        job.delete()
        return JsonResponse({'success': True})
    except JobDetail.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)


