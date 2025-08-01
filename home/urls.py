from django.urls import path
from . import views
from .views import download_CVpdf

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('download-cv/<int:pk>/', download_CVpdf, name='download_cv'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail')
    ]
