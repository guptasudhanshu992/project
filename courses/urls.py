from django.urls import path
from .views import PublishedCourseCardsView, CourseOverviewAPIView, TopicDetailsAPIView


urlpatterns = [
    path('coursecards/', PublishedCourseCardsView.as_view(), name='coursecardapi'),
    path('<slug:slug>', CourseOverviewAPIView.as_view(), name='courseoverviewapi'),
    path('topic/<uuid:id>', TopicDetailsAPIView.as_view(), name='topicdetailsapi'),
]