from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserApiViewSet, UserView

router = DefaultRouter()
router.register('users', UserApiViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/me/', UserView.as_view(), name='auth-me'),
]
