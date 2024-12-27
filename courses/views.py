from django.shortcuts import render
from django.views import View
from .models import Course, Lesson
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.http import Http404

class CourseView(View):
    def get(self, request):
        live_courses = Course.objects.all()
        context = {
            "live_courses":live_courses,
        }

        return render(request, 'courses.html', context)

class CourseDetailsView(DetailView):
    model = Course
    template_name = 'course_details.html'
    context_object_name = 'course_details'

    def get_object(self):
        course_url = self.kwargs.get('course_url')
        course_details = get_object_or_404(Course, course_url=course_url, status_live=True)

        if not course_details.status_live:
            raise Http404("Course is not live")

        return course_details

class LessonView(DetailView):
    model = Lesson
    template_name = 'lesson.html'
    context_object_name = 'lesson_details'

    def get_object(self):
        lesson_id = self.kwargs.get('lesson_id')
        lesson_details = get_object_or_404(Lesson, id=lesson_id)

        return lesson_details
