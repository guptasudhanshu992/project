from rest_framework import serializers
from .models import Blog, BlogSection, Category

class BlogSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
        required=False
    )

    class Meta:
        model = Blog
        fields = [
            'title', 
            'slug', 
            'snippet_json', 
            'author', 
            'category', 
            'featured_image', 
            'updated_at',
            'published_at',
            'reading_time'
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'name']

class BlogDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    #sections = BlogSectionSerializer(source='sections.all', many=True, read_only=True)
    
    class Meta:
        model = Blog
        fields = [
            'blog_id',
            'title',
            'slug',
            'content_json',
            'updated_at',
            'reading_time',
            'category',
            #'sections',
        ]
