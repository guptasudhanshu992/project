from rest_framework import serializers
from .models import Course, Category, CourseTopic

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        
class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Course
        fields = [
            "id",
            "slug",
            "title",
            "cover_image",
            "price",
            "short_description",
            "long_description",
            "learning_outcomes",
            "pre_requisites",
            "language",
            "preview_video",
            "category",
            "updated_at",
            "published_at"
        ]

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseTopic
        fields = [
            "id",
            "chapter",
            "title",
            "video_url",
            "content",
            "order",
            "created_at",
            "updated_at",
        ]