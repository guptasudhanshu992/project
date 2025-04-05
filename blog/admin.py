from django.contrib import admin
from .models import Blog, Category, Tag, BlogTag, BlogCategory, BlogSection

class BlogTagInline(admin.TabularInline):
    model = BlogTag
    extra = 1

class BlogCategoryInline(admin.TabularInline):
    model = BlogCategory
    extra = 1

class BlogSectionInline(admin.StackedInline):
    model = BlogSection
    extra = 1
    fields = ('content_text', 'section_image', 'section_image_alt', 'section_video_url')
    show_change_link = True

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'updated_at', 'published_at')
    list_filter = ('status', 'created_at', 'updated_at', 'published_at', 'category')
    search_fields = ('title', 'content', 'seo_title', 'seo_description', 'seo_keywords')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlogSectionInline, BlogTagInline, BlogCategoryInline]
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fields = (
        'title', 'slug', 'snippet', 'snippet_json', 'content_json', 'author', 'category', 'status',
        'seo_title', 'seo_description', 'seo_keywords',
        'featured_image', 'created_at', 'updated_at', 'published_at'
    )
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('-created_at',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('-created_at',)

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('blog', 'tag')
    search_fields = ('blog__title', 'tag__name')

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('blog', 'category')
    search_fields = ('blog__title', 'category__name')
