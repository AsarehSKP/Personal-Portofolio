from django.urls import path
from .views import ProjectDetailView

app_name = 'resume'  # مثلاً برای پروژه‌ها

urlpatterns = [
    path('projects/<slug:slug>/', ProjectDetailView.as_view(), name='project_detail'),
]
