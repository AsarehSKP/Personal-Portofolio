from django.urls import path
from . import views
from .views import BlogListView,BlogDetailView

app_name = 'blog_app'
urlpatterns = [
    # path('post/', views.post_detail, name='post_detail'),
    path('service/<slug:slug>/', views.service_view, name='service_detail'),
    path('blog/', BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
]
