from django import template
from blog_app.models import BlogPost
from resume.models import Project

register = template.Library()


@register.simple_tag()
def total_posts():
    return BlogPost.objects.count()


@register.simple_tag()
def total_projects():
    return Project.objects.count()


@register.inclusion_tag("partials/latest_posts.html")
def latest_posts(count=6):
    l_posts = BlogPost.objects.published()[:count]
    context = {'l_posts': l_posts}
    return context
