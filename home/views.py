from django.shortcuts import render,redirect
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from .models import *
from blog_app.models import Service,BlogPost
from resume.models import *
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

    try:
        cv = CV_pdf.objects.latest('created_at')  # یا هر شرط خاص
    except CV_pdf.DoesNotExist:
        cv = None

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
        'cv': cv,
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


def download_CVpdf(request, pk):
    cv = CV_pdf.objects.get(pk=pk)
    html_string = render_to_string('home/cv_pdf.html', {'cv': cv})
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{cv.first_name}_{cv.last_name}_CV.pdf"'
    return response

