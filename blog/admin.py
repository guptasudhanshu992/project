from django.contrib import admin
from .models import BlogPost, BlogSection, Category

class BlogSectionInline(admin.StackedInline):
    model = BlogSection
    extra = 1

class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"post_url": ("title",)}
    inlines = [BlogSectionInline]

#@admin.register(BlogPost)
#class BlogPostAdmin(admin.ModelAdmin):
#    list_display = ('title', 'updated_at', 'published_at', 'status_live')
#    search_fields = ('title',)
#    list_filter = ('updated_at', 'published_at', 'status_live',)
#    filter_horizontal = ('categories',)

admin.site.register(Category)
admin.site.register(BlogPost, BlogPostAdmin)