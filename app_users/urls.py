from django.urls import path
from app_users.views import AnotherLoginView, AnotherLogoutView, register_view, ProfileView, RedactProfileView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', AnotherLoginView.as_view(), name='login'),
    path('logout/', AnotherLogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit', RedactProfileView.as_view(), name='user-profile-edit')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

