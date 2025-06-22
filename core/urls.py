from django.urls import path
from .views import HomeView, BlogView, LoginView, RegisterView, CoursesView, AboutView, ProfileView, BlogDetailsView, CourseDetailsView, CourseContentsView, CartView, WishlistView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #path('', HomeView.as_view(), name='homeview'),
    path('', BlogView.as_view(), name='blogview'),
    path('blog/', BlogView.as_view(), name='blogview'),
    path('blog/<slug:slug>', BlogDetailsView.as_view(), name='blogdetailsview'),
    path('courses/', CoursesView.as_view(), name='coursesview'),
    path('about/', AboutView.as_view(), name='aboutview'),
    path('login/', LoginView.as_view(), name='loginview'),
    path('register/', RegisterView.as_view(), name='registerview'),
    path('profile/', ProfileView.as_view(), name='profileview'),
    path('courses/<slug:slug>/', CourseDetailsView.as_view(), name='course_details_view'),
    path('courses/contents/<slug:slug>/', CourseContentsView.as_view(), name='course_contents_view'),
    path('cart/', CartView.as_view(), name='cartview'),
    path('wishlist/', WishlistView.as_view(), name='wishlistview'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)