from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lesson

@receiver(post_save, sender=Lesson)
def update_course_content(sender, instance, **kwargs):
    course = instance.chapter.course

    course_hierarchy = []
    for chapter in course.chapters.all():
        chapter_data = {
            'chapter_name': chapter.title,
            'lessons': [{'lesson_name': lesson.title, 'lesson_id': lesson.id} for lesson in chapter.lessons.all()]
        }
        course_hierarchy.append(chapter_data)

    course.course_content = course_hierarchy
    course.save()
