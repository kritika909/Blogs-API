from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'profiles', ProfileViewSet, basename='profile')

# urlpatterns = [
#     path('', include(router.urls)),
#     path('', include(router.urls)),
# ]

urlpatterns = router.urls