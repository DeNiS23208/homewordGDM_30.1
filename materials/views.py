from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModeratorCanOnlyChange, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .models import Subscription
from .serializers import SubscriptionSerializer
from .paginators import MyPagination


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModeratorCanOnlyChange, IsOwnerOrReadOnly]
    pagination_class = MyPagination

    def get_queryset(self):
        queryset = Course.objects.all()
        if self.request.user.groups.filter(name="Модераторы").exists():
            return queryset
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorCanOnlyChange, IsOwnerOrReadOnly]
    pagination_class = MyPagination

    def get_queryset(self):
        queryset = Lesson.objects.all()
        if self.request.user.groups.filter(name="Модераторы").exists():
            return queryset
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModeratorCanOnlyChange, IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Lesson.objects.all()
        if self.request.user.groups.filter(name="Модераторы").exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionDeleteAPIView(generics.DestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)
