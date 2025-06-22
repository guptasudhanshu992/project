from rest_framework import serializers
from .models import Blog, BlogCategory, BlogTag
from userauthentication.models import NewUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class BlogSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='email',
        queryset=NewUser.objects.all(),
        required=False
    )
    
    class Meta:
        model = Blog
        fields = [
            'title', 
            'slug', 
            'snippet',
            'author', 
            'category', 
            'cover_image', 
            'updated_at',
            'published_at',
            'reading_time'
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['name']

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = ['name']

class BlogDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=BlogCategory.objects.all(),
        required=False
    )
    
    tag = serializers.SlugRelatedField(
        slug_field='name',
        queryset=BlogTag.objects.all(),
        required=False
    )
    
    class Meta:
        model = Blog
        fields = [
            'id',
            'title',
            'slug',
            'snippet',
            'content',
            'updated_at',
            'reading_time',
            'category',
            'tag',
        ]
