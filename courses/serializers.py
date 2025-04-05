from rest_framework import serializers
from .models import Course, CourseCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['category_id', 'name']
        
class CourseSerializer(serializers.ModelSerializer):
    course_category = CategorySerializer(CourseCategory.objects.all(), many=False)

    class Meta:
        model = Course
        fields = [
            "course_id",
            "title",
            "course_url",
            "course_image",
            "price",
            "short_description",
            "language",
            "preview_video",
            "course_category",
            "published_at"
        ]