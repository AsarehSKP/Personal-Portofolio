from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import Project


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'resume/projectdetail.html'  # مسیر تمپلیت که الان ساختیم
    context_object_name = 'project'


