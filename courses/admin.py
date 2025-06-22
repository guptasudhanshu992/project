from django.contrib import admin
from .models import (
    TargetAudienceDescription, PreRequisiteDescription, LearningOutcomeDescription,
    Language, Category, Course, CourseChapter, CourseTopic, CourseQuiz, QuizQuestion, QuestionOption,
    QuestionAnswerMapping, Enrollment, Review, Features, Tags, SkillLevel
)


# ========== Inline Models ==========

class CourseChapterInline(admin.StackedInline):
    model = CourseChapter
    extra = 1


class CourseTopicInline(admin.StackedInline):
    model = CourseTopic
    extra = 1


class CourseQuizInline(admin.StackedInline):
    model = CourseQuiz
    extra = 1


class QuizQuestionInline(admin.StackedInline):
    model = QuizQuestion
    extra = 1


class QuestionOptionInline(admin.StackedInline):
    model = QuestionOption
    extra = 1


# ========== Admin Model Configurations ==========

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'duration', 'created_at')
    prepopulated_fields = {'slug': ('title',)}  # Auto fill slug from title
    fields = (
        'title', 'slug', 'cover_image', 'cover_image_alt', 'preview_video',
        'price', 'short_description', 'long_description', 'has_certificate', 'skilllevel', 'tags', 'instructor', 'features', 
        'category', 'language', 'status', 'published_at', 'duration', 'course_structure',
        'target_audience', 'pre_requisites', 'learning_outcomes',
    )
    search_fields = ('title', 'slug')
    list_filter = ('status', 'category', 'language')

admin.site.register(Course, CourseAdmin)


@admin.register(CourseChapter)
class CourseChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    ordering = ['course', 'order']
    inlines = [CourseTopicInline, CourseQuizInline]


@admin.register(CourseTopic)
class CourseTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'order')
    list_filter = ('chapter__course',)
    search_fields = ('title', 'chapter__title')
    ordering = ['chapter', 'order']


@admin.register(CourseQuiz)
class CourseQuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter')
    search_fields = ('title', 'chapter__title')
    inlines = [QuizQuestionInline]


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'quiz')
    inlines = [QuestionOptionInline]


@admin.register(QuestionAnswerMapping)
class QuestionAnswerMappingAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')
    list_filter = ('created_at', 'course')
    search_fields = ('user__username', 'course__title')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'rating', 'review_date')
    list_filter = ('course', 'rating', 'review_date')
    search_fields = ('student__username', 'course__title')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(SkillLevel)
class SkillLevelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(TargetAudienceDescription)
class TargetAudienceDescriptionAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ('description',)


@admin.register(PreRequisiteDescription)
class PreRequisiteDescriptionAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ('description',)


@admin.register(LearningOutcomeDescription)
class LearningOutcomeDescriptionAdmin(admin.ModelAdmin):
    list_display = ('description',)
    search_fields = ('description',)

@admin.register(Features)
class FeaturesAdmin(admin.ModelAdmin):
    list_display = ('icon', 'description',)
    search_fields = ('description',)