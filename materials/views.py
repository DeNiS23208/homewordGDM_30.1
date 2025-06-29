from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModeratorCanOnlyChange, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsModeratorCanOnlyChange, IsOwnerOrReadOnly]

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
