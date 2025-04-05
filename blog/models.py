from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from bs4 import BeautifulSoup
from django.db.models.signals import post_save
from django.dispatch import receiver
import json
import math
from django.db import transaction
from django_ckeditor_5.fields import CKEditor5Field


User = get_user_model()


def html_to_json(html_content: str) -> str:
    soup = BeautifulSoup(html_content, 'html.parser')

    content = []
    stack = []

    def add_to_parent(element):
        if stack:
            parent = stack[-1]
            if 'content' not in parent:
                parent['content'] = []
            parent['content'].append(element)
        else:
            content.append(element)

    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'img', 'video']):
        if element.name in ['h1', 'h2', 'h3']:
            level = int(element.name[1])

            while stack and int(stack[-1]['type'][1]) >= level:
                stack.pop()

            heading = {"type": element.name, "text": element.get_text(strip=True), "content": []}
            add_to_parent(heading)

            stack.append(heading)

        elif element.name == 'p':
            paragraph = {"type": "p", "text": element.get_text(strip=True)}
            add_to_parent(paragraph)

        elif element.name in ['img', 'video']:
            media = {
                "type": "image" if element.name == "img" else "video",
                "src": element.get('src'),
                "alt": element.get('alt', '') if element.name == "img" else '',
                "controls": element.has_attr('controls') if element.name == 'video' else None,
                "autoplay": element.has_attr('autoplay') if element.name == 'video' else None
            }
            add_to_parent(media)

    return json.dumps({"content": content}, separators=(',', ':'))


class Category(models.Model):
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

class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Blog(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    blog_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    snippet = CKEditor5Field('Text', config_name='extends',null=True, blank=True)
    snippet_json = models.JSONField(blank=True, null=True)
    content_json = models.JSONField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    seo_title = models.CharField(max_length=200, blank=True)
    seo_description = models.TextField(blank=True)
    seo_keywords = models.CharField(max_length=255, blank=True)
    featured_image = models.ImageField(upload_to='static/blogs/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, through='BlogTag')
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, blank=True)
    published_at = models.DateTimeField(default=timezone.now, blank=True)
    reading_time = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title

class BlogSection(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="sections")
    content_text = CKEditor5Field('Text', config_name='extends',null=True, blank=True)
    section_image = models.ImageField(upload_to='blogs/', null=True, blank=True)
    section_image_alt = models.CharField(max_length=255, null=True, blank=True)
    section_video_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"Section of {self.blog.title}"

class BlogTag(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('blog', 'tag')

class BlogCategory(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('blog', 'category')

@receiver(post_save, sender=BlogSection)
def update_blogpost_word_count(sender, instance, **kwargs):
    blog = instance.blog

    total_words = sum(
        len((section.content_text or "").strip().split()) for section in blog.sections.all()
    )

    if instance.content_text:
        total_words += len(instance.content_text.strip().split())

    blog.reading_time = max(1, math.ceil(total_words / 200)) 
    blog.save(update_fields=['reading_time']) 

@receiver(post_save, sender=Blog)
def process_blog_content(sender, instance, **kwargs):
    combined_content = ""
    for section in instance.sections.all():
        if section.content_text:
            combined_content += f"{section.content_text}"
        if section.section_image:
            combined_content += f'<img src="{section.section_image.url}" alt="{section.section_image_alt or ""}">'
        if section.section_video_url:
            combined_content += f'<video src="{section.section_video_url}" controls></video>'

    new_content_json = html_to_json(combined_content)
    new_snippet_json = html_to_json(instance.snippet)
    
    if instance.snippet_json != new_snippet_json:
        def update_snippet():
            instance.snippet_json = new_snippet_json
            instance.save(update_fields=['snippet_json'])
        transaction.on_commit(update_snippet)

    if instance.content_json != new_content_json:
        def update_content():
            instance.content_json = new_content_json
            instance.save(update_fields=['content_json'])

        transaction.on_commit(update_content)

