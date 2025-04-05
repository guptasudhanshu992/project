from django.http import JsonResponse
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Course, CourseCategory
from .serializers import CourseSerializer, CategorySerializer
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from rest_framework import status
import time

class PublishedCourseCardsView(View):
    def get(self, request, *args, **kwargs):
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 12)
        category = request.GET.get('category', 'all')
        
        queryset = Course.objects.filter(status='published').order_by('-published_at')
        if category and category.lower() != "all":
            queryset = queryset.filter(category__name__iexact=category)

        paginator = Paginator(queryset, page_size)
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        serializer = CourseSerializer(blogs, many=True)

        categories = CourseCategory.objects.all()
        category_serializer = CategorySerializer(CourseCategory.objects.all(), many=True)
        
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

class CourseOverviewAPIView(View):
    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        serializer = CourseSerializer(course)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)