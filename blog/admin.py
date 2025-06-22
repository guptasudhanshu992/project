from django.contrib import admin
from .models import BlogCategory, BlogTag, Blog

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'slug', 'status', 'author',
        'display_categories', 'display_tags',
        'reading_time', 'published_at'
    )
    list_filter = ('status', 'author', 'category', 'tags')
    search_fields = ('title', 'snippet')
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('reading_time', 'published_at', 'updated_at')

    # Allows adding new tags/categories directly from Blog form
    filter_horizontal = ('category', 'tags')

    def display_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
    display_tags.short_description = 'Tags'

    def display_categories(self, obj):
        return ", ".join(category.name for category in obj.category.all())
    display_categories.short_description = 'Categories'
