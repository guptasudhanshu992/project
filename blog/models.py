from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Category"

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200, unique=True)
    post_url = models.SlugField(max_length=200, unique=True, blank=True)
    cover_image = models.ImageField(upload_to="media/blog_images/", blank=True, null=True)
    cover_image_alt = models.CharField(max_length=255, blank=True, null=True)
    snippet = RichTextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateField(default=now)
    published_at = models.DateTimeField(default=now)
    status_live = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, related_name='blog_posts', blank=True)
    reading_time = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.post_url:
            self.post_url = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class BlogSection(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="sections")
    section_title = models.CharField(max_length=255, null=True, blank=True)
    content_text = RichTextField(null=True, blank=True)
    section_image = models.ImageField(upload_to='media/blog_images/', null=True, blank=True)
    section_image_alt = models.CharField(max_length=255, null=True, blank=True)
    section_video_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"Section of {self.blog_post.title}: {self.section_title if self.section_title else 'Untitled'}"

@receiver(post_save, sender=BlogSection)
def update_blogpost_word_count(sender, instance, **kwargs):
    blog_post = instance.blog_post

    total_words = sum(
        len(section.content_text.split()) for section in blog_post.sections.all() if section.content_text
    )

    blog_post.reading_time = total_words/200
    blog_post.save()