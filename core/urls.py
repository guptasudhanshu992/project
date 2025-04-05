from django.urls import path
from .views import HomeView, BlogView, LoginView, RegisterView, CoursesView, AboutView, ProfileView, BlogDetailsView, CourseDetailsView, LessonView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', HomeView.as_view(), name='homeview'),
    path('blog/', BlogView.as_view(), name='blogview'),
    path('blog/<slug:slug>', BlogDetailsView.as_view(), name='blogdetailsview'),
    path('courses/', CoursesView.as_view(), name='coursesview'),
    path('about/', AboutView.as_view(), name='aboutview'),
    path('login/', LoginView.as_view(), name='loginview'),
    path('register/', RegisterView.as_view(), name='registerview'),
    path('profile/', ProfileView.as_view(), name='profileview'),
    path('courses/<slug:slug>/', CourseDetailsView.as_view(), name='course_details_view'),
    path('<slug:course_url>/<int:lesson_id>/', LessonView.as_view(), name='lesson_view'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)