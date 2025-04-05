from django.contrib import admin
from .models import Course, Chapter, Lesson, CourseCategory

"""admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Lesson)
"""

@admin.register(CourseCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('-created_at',)

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1
    fields = ('title',)


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('title', 'order', 'content')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    inlines = [ChapterInline,]


class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at', 'updated_at')
    search_fields = ('title',)
    fieldsets = (
        (None, {
            'fields': ('title', 'course', 'order',)
        }),
    )
    inlines = [LessonInline,]


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'order',)
    search_fields = ('title', 'chapter',)
    fieldsets = (
        (None, {
            'fields': ('title', 'order', 'chapter', 'video_url', 'content')
        }),
    )

"""class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at', 'updated_at')
    search_fields = ('title',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'location', 'course', 'chapter', 'lesson', 'created_at', 'updated_at')
        }),
    )
"""
admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Lesson, LessonAdmin)
#admin.site.register(Quiz, QuizAdmin)

