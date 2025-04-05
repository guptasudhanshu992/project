from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field

User = get_user_model()


class CourseCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
        
class Course(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    course_id = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=200, unique=True)
    course_url = models.SlugField(max_length=200, unique=True, blank=True)
    course_image = models.ImageField(upload_to="static/course_images/", blank=True, null=True)
    course_image_alt = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=8, null=True, decimal_places=2)
    short_description = CKEditor5Field('Short Description', config_name='extends',null=True, blank=True)
    long_description = CKEditor5Field('Long Description', config_name='extends',null=True, blank=True)
    learning_outcomes = CKEditor5Field('Learning Outcomes', config_name='extends',null=True, blank=True)
    pre_requisites = CKEditor5Field('Pre Requisites', config_name='extends',null=True, blank=True)
    who_is_the_course_for = CKEditor5Field('who_is_the_course_for', config_name='extends',null=True, blank=True)
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    language = models.CharField(max_length=50, default="English")
    preview_video = models.URLField(blank=True, null=True)
    course_card_json = models.JSONField(blank=True, null=True)
    course_overview_json = models.JSONField(blank=True, null=True)
    course_content_json = models.JSONField(blank=True, null=True)
    course_category = models.ForeignKey(CourseCategory, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        if not self.course_url:
            self.course_url = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class CourseCategoryMapping(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'category')
        
class Chapter(models.Model):
    chapter_id = models.CharField(max_length=10, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(help_text="Order of the chapter in the course")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} - {self.course.title}"


class Lesson(models.Model):
    lesson_id = models.CharField(max_length=10, unique=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = CKEditor5Field('Text', config_name='extends',null=True, blank=True)
    order = models.PositiveIntegerField(help_text="Order of the lesson in the chapter")
    video_url = models.URLField(blank=True, null=True, help_text="Optional video link for the lesson")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} - {self.chapter.title}"

"""
class Quiz(models.Model):
    QUIZ_LOCATION_CHOICES = [
        ('course', 'Course Level'),
        ('chapter', 'Chapter Level'),
        ('lesson', 'Lesson Level'),
    ]

    title = models.CharField(max_length=200)
    description = RichTextField(blank=True, null=True)
    location = models.CharField(max_length=10, choices=QUIZ_LOCATION_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quizzes', blank=True, null=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='quizzes', blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Quiz"

    def clean(self):
        '''
        Ensures the quiz is associated with exactly one location (course, chapter, or lesson).
        '''
        selected_levels = [self.course, self.chapter, self.lesson]
        if sum(bool(level) for level in selected_levels) != 1:
            raise ValueError("A quiz must be assigned to exactly one level: course, chapter, or lesson.")

    def __str__(self):
        return f"Quiz: {self.title} ({self.get_location_display()})"


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollments")
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="enrollments")
    enrollment_date = models.DateTimeField(auto_now_add=True)
    progress = models.JSONField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    certificate_url = models.URLField(blank=True, null=True)
    rating = models.FloatField(default=0.0)
    feedback = RichTextField()

    class Meta:
        unique_together = ("student", "course")  # Ensures a student can't enroll in the same course twice
        ordering = ["-enrollment_date"]  # Orders enrollments by most recent first

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
"""