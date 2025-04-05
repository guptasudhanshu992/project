from django.urls import path
from . import views
from .views import PublishedBlogPaginatedView, BlogDetailAPIView

urlpatterns = [
    path('blog-articles/', PublishedBlogPaginatedView.as_view(), name='blogapi'),
    path('blog-articles/<slug:slug>', BlogDetailAPIView.as_view(), name='blogdetailsapi'),
]