from django.shortcuts import render,redirect
from .models import *
from blog_app.models import Service,BlogPost
from resume.models import Project, Resume
from django.contrib import messages


# Create your views here.
def home(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    services = Service.objects.published()
    latest_posts = BlogPost.objects.all()[:3]
    latest_projects = Project.objects.all()[:6]
    about = About.objects.first()
    site_info = About.objects.first()

    resume_left = Resume.objects.filter(column='left')
    resume_right = Resume.objects.filter(column='right')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        if name and email and subject and message:
            Contact.objects.create(name=name, email=email, subject=subject, message=message)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('home:home')
        else:
            messages.error(request, 'Please fill all the fields')

    context = {
        'about': about,
        'profile': profile,
        'skills': skills,
        'services': services,
        'latest_posts': latest_posts,
        'latest_projects': latest_projects,
        'site_info': site_info,
        'resume_left': resume_left,
        'resume_right': resume_right
    }

    return render(request, 'home/index.html', context)
