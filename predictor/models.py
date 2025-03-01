# predictor/models.py
from django.db import models

class Prediction(models.Model):
    username = models.CharField(max_length=150)
    predicted_title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.predicted_title}"




from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length=255)
    company_location = models.CharField(max_length=255)
    company_email = models.EmailField(unique=True)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    password = models.CharField(max_length=128)  # In production, use Django's built-in User model

    def __str__(self):
        return self.company_name

class JobDetail(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_details')
    job_title = models.CharField(max_length=255)
    # We have 5 skills fields in the form.
    # One approach is to store them as a comma-separated string:
    skills = models.CharField(max_length=1024, help_text="Enter skills separated by commas")

    def __str__(self):
        return f"{self.job_title} ({self.company.company_name})"
