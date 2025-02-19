from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import LoginAPIView, SignUpAPIView, LogoutAPIView


urlpatterns = [
    path('', SignUpAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
