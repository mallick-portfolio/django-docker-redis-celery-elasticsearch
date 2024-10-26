from .views import PostViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', PostViewSet, basename='post')
urlpatterns = [
    # path('forgot-password/', ForgotPasswordFormView.as_view()),
]
urlpatterns = router.urls