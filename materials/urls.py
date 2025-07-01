from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    LessonListCreateAPIView,
    LessonRetrieveUpdateDestroyAPIView, SubscriptionCreateAPIView, SubscriptionDeleteAPIView
)

router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListCreateAPIView.as_view(), name="lesson-list-create"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDestroyAPIView.as_view(),
        name="lesson-detail",
    ),
    path('subscriptions/', SubscriptionCreateAPIView.as_view(), name='subscription-create'),
    path('subscriptions/<int:pk>/', SubscriptionDeleteAPIView.as_view(), name='subscription-delete'),
]
