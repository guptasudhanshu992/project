from django.urls import path
from .views import BlogView, BlogPostView


urlpatterns = [
    path('', BlogView.as_view(), name='blog_view'),
    path('blog/<slug:post_url>', BlogPostView.as_view(), name='blog_post_view'),

]