from django.http import JsonResponse
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Blog, Category
from .serializers import BlogSerializer, BlogDetailSerializer, CategorySerializer
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from rest_framework import status
import time
 
class PublishedBlogPaginatedView(View):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 12)
        category = request.GET.get('category')
        
        queryset = Blog.objects.filter(status='published').order_by('-published_at')
        if category and category.lower() != "all":
            queryset = queryset.filter(category__name__iexact=category)

        paginator = Paginator(queryset, page_size)
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        serializer = BlogSerializer(blogs, many=True)

        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)
        
        response = {
            'data': serializer.data,
            'categories': category_serializer.data,
            'pagination': {
                'total_pages': paginator.num_pages,
                'current_page': blogs.number,
                'has_next': blogs.has_next(),
                'has_previous': blogs.has_previous(),
                'total_items': paginator.count,
            }
        }
        return JsonResponse(response, safe=False)
        
class BlogDetailAPIView(View):
    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)
        serializer = BlogDetailSerializer(blog)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)