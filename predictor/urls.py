# predictor/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),           # Homepage (Home.html)
    path('register/', views.register, name='register'),  # Registration view
    path('explore/', views.explore, name='explore'),  # Prediction form (explore.html)
    path('post/', views.post, name='post'),
    path('create_company/', views.create_company, name='create_company'),
    path('post_job/', views.post_job, name='post_job'),
    path('job/', views.job, name='job'),
    path('login/', views.login_view, name='login'),  # Login view
    path('recommend/', views.recommend_view, name='recommend'),
    path('company_signin/', views.company_signin, name='company_signin'),
    path('company/', views.company, name='company'),
    path('remove_job/<int:job_id>/', views.remove_job, name='remove_job'),
]
