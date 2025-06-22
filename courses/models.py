from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django_ckeditor_5.fields import CKEditor5Field
import uuid

User = get_user_model()

# ========== Reusable Description Models ==========

class TargetAudienceDescription(models.Model):
    description = models.TextField('Target Audience Description', unique=True)
    class Meta:
        verbose_name_plural = "Target Audience Descriptions"

    def __str__(self):
        return self.description[:50] + "..." if len(self.description) > 50 else self.description


class PreRequisiteDescription(models.Model):
    description = models.TextField('Pre-requisite Description', unique=True)
    class Meta:
        verbose_name_plural = "Pre-requisite Descriptions"

    def __str__(self):
        return self.description[:50] + "..." if len(self.description) > 50 else self.description


class LearningOutcomeDescription(models.Model):
    description = models.TextField('Learning Outcome Description', unique=True)
    class Meta:
        verbose_name_plural = "Learning Outcome Descriptions"

    def __str__(self):
        return self.description[:50] + "..." if len(self.description) > 50 else self.description


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="e.g., English, Spanish, French")

    def __str__(self):
        return self.name

class SkillLevel(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="e.g., Beginner, Intermediate, Advanced")

    def __str__(self):
        return self.name
        
class Features(models.Model):
    icon = models.TextField('icon')
    description = models.TextField('Course Features', unique=True)
    class Meta:
        verbose_name_plural = "Course Features"

    def __str__(self):
        return self.description[:50] + "..." if len(self.description) > 50 else self.description

# ========== Core Models ==========

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    cover_image = models.ImageField(upload_to="course_images/", blank=True, null=True)
    cover_image_alt = models.CharField(max_length=255, blank=True, null=True)
    preview_video = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, null=True, decimal_places=2)
    short_description = CKEditor5Field('Short Description', config_name='extends', null=True, blank=True)
    long_description = CKEditor5Field('Long Description', config_name='extends', null=True, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructed_courses')
    enrollments = models.PositiveIntegerField(default=0)
    reviews = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(default=0.00, max_digits=3, decimal_places=2)
    skilllevel = models.ManyToManyField(
        SkillLevel,
        blank=True,
        related_name='skill_levels_for_the_course',
        help_text="The Skill Level for the course."
    )
    has_certificate = models.BooleanField(
        default=False,
        help_text="Check if this course provides a certificate upon completion."
    )
    duration = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        help_text="Total duration of the course in hours"
    )
    category = models.ManyToManyField(
        Category,
        blank=True,
        related_name='courses_in_this_category',
        help_text="The category of this course."
    )
    language = models.ManyToManyField(
        Language,
        blank=True,
        related_name='courses_in_this_language',
        help_text="The language of this course."
    )
    features = models.ManyToManyField(
        Features,
        blank=True,
        related_name='course_features',
        help_text="The Features of the Course."
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now, blank=True)
    course_structure = models.JSONField(blank=True, null=True)
    target_audience = models.ManyToManyField(
        TargetAudienceDescription,
        blank=True,
        related_name='courses_for_this_audience'
    )
    pre_requisites = models.ManyToManyField(
        PreRequisiteDescription,
        blank=True,
        related_name='courses_with_these_prerequisites'
    )
    learning_outcomes = models.ManyToManyField(
        LearningOutcomeDescription,
        blank=True,
        related_name='courses_with_these_outcomes'
    )
    tags = models.ManyToManyField(
        Tags,
        blank=True,
        related_name='courses_with_these_tags',
        help_text="The Tags of this course."
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CourseChapter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(help_text="Order of the chapter in the course")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} (Course: {self.course.title})"


class CourseTopic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    video_url = models.URLField(blank=True, null=True)
    content = CKEditor5Field('Content', config_name='extends', null=True, blank=True)
    order = models.PositiveIntegerField(help_text="Order of the topics in the chapter")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} (Chapter: {self.chapter.title})"

class CourseQuiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)
    json = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (Chapter: {self.chapter.title})"


class QuizQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(CourseQuiz, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=250)

    def __str__(self):
        return f"Question: {self.question}"


class QuestionOption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='options')
    option = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.option} (Question: {self.question.question})"


class QuestionAnswerMapping(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    answer = models.ForeignKey(QuestionOption, on_delete=models.CASCADE)

    def __str__(self):
        return f"Answer to '{self.question.question}' is '{self.answer.option}'"


class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'user'], name='unique_course_user_enrollment')
        ]

    def __str__(self):
        return f"{self.user} enrolled in {self.course.title}"


class Review(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='course_reviews'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='course_reviews'
    )
    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0)
        ]
    )
    like_note = models.TextField(blank=True)
    dislike_note = models.TextField(blank=True)
    review_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'course', 'enrollment'], name='unique_review')
        ]

    def __str__(self):
        return f"Review for {self.course.title} by {self.student} - Rating: {self.rating}"

#Signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count

@receiver(post_save, sender=Enrollment)
def update_course_enrollment_count(sender, instance, created, **kwargs):
    if created:
        course = instance.course
        course.enrollments = Enrollment.objects.filter(course=course).count()
        course.save(update_fields=['enrollments'])

@receiver(post_delete, sender=Enrollment)
def decrement_course_enrollment_count(sender, instance, **kwargs):
    course = instance.course
    course.enrollments = Enrollment.objects.filter(course=course).count()
    course.save(update_fields=['enrollments'])

@receiver(post_save, sender=Review)
def update_course_review_stats(sender, instance, created, **kwargs):
    course = instance.course
    stats = Review.objects.filter(course=course).aggregate(
        avg_rating=Avg('rating'),
        review_count=Count('id')
    )
    course.rating = round(stats['avg_rating'] or 0, 2)
    course.reviews = stats['review_count']
    course.save(update_fields=['rating', 'reviews'])

@receiver(post_delete, sender=Review)
def recalculate_course_review_stats(sender, instance, **kwargs):
    course = instance.course
    stats = Review.objects.filter(course=course).aggregate(
        avg_rating=Avg('rating'),
        review_count=Count('id')
    )
    course.rating = round(stats['avg_rating'] or 0, 2)
    course.reviews = stats['review_count']
    course.save(update_fields=['rating', 'reviews'])

