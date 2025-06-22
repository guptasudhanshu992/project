from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CourseTopic, Course
import json

@receiver(post_save, sender=CourseTopic)
def update_course_structure(sender, instance, **kwargs):
    chapter = instance.chapter
    course = chapter.course

    structure = []

    chapters = course.chapters.all().order_by('order')
    for ch in chapters:
        topics = ch.topics.all().order_by('order')
        topic_list = []
        for tp in topics:
            topic_list.append({
                "id": str(tp.id),
                "title": tp.title,
                "video_url": tp.video_url,
                "content": tp.content,
                "order": tp.order,
            })
        structure.append({
            "id": str(ch.id),
            "title": ch.title,
            "order": ch.order,
            "topics": topic_list
        })

    course.course_structure = {
        "course_id": str(course.id),
        "title": course.title,
        "chapters": structure
    }
    course.save()

@receiver(post_save, sender=Course)
def update_course_card_json(sender, instance, created, **kwargs):
    course_card_data = {
        "title": instance.title,
        "slug": instance.slug,
        "cover_image": instance.cover_image.url if instance.cover_image else None,
        "price": str(instance.price) if instance.price else None,
        "short_description": instance.short_description,
        "instructor": instance.instructor.email,
        "language": instance.language,
        "preview_video": instance.preview_video,
        "category": instance.category.name if instance.category else None,
    }
