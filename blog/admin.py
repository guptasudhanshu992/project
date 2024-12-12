from django.contrib import admin
from .models import BlogPost, Category

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at', 'published_at', 'status_live')
    search_fields = ('title',)
    list_filter = ('updated_at', 'published_at', 'status_live',)
    filter_horizontal = ('categories',)

admin.site.register(Category)