from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('download-resume/', download_resume_pdf, name='download_resume_pdf'),
    ]
