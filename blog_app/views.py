from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView, DetailView


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog_app/bloglist.html'
    context_object_name = 'blog_list'
    paginate_by = 3

    def get_queryset(self):
        return BlogPost.objects.published()


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_app/single.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # اگر بخوای پست‌های مرتبط یا اخیر رو هم اضافه کنی
        context['recent_posts'] = BlogPost.objects.published().exclude(pk=self.object.pk)[:3]
        return context




def service_view(request, slug):
    service = get_object_or_404(Service.objects.published(), slug=slug)
    context = {'service': service}
    return render(request, 'blog_app/service_detail.html', context)

