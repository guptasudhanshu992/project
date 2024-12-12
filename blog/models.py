from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200, unique=True)
    post_url = models.SlugField(max_length=200, unique=True, blank=True)
    image = models.ImageField(upload_to="media/blog_images/", blank=True, null=True)
    image_alt = models.CharField(max_length=255, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateField(default=now)
    published_at = models.DateTimeField(default=now)
    content = RichTextField()
    status_live = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, related_name='blog_posts', blank=True)

    def save(self, *args, **kwargs):
        if not self.post_url:
            self.post_url = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)

    @property
    def number_of_words(self):
        return len(self.content.split())

    @property
    def reading_time(self):
        words_per_minute = 200
        return max(1, self.number_of_words // words_per_minute)

    def __str__(self):
        return self.title
