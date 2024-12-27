from django.urls import path
from .views import CourseView, CourseDetailsView, LessonView


urlpatterns = [
    path('', CourseView.as_view(), name='course_view'),
    path('<slug:course_url>/', CourseDetailsView.as_view(), name='course_details_view'),
    path('<slug:course_url>/<int:lesson_id>/', LessonView.as_view(), name='lesson_view'),

]