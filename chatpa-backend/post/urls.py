from .views import PostViewSet, SearchPost
from rest_framework.routers import DefaultRouter
from  django.urls import path, include

router = DefaultRouter()
router.register(r'', PostViewSet, basename='post')
urlpatterns = [
    path("search/<str:query>/", SearchPost.as_view()),
]
urlpatterns += router.urls