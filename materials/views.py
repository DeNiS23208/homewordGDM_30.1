from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModeratorCanOnlyChange, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .models import Subscription
from .serializers import SubscriptionSerializer
from .paginators import MyPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from .stripe_service import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_session,
)
from .models import Course, Payment, Lesson
from .tasks import notify_subscribers_about_new_lesson
from users.tasks import send_mass_mailing


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

    def perform_update(self, serializer):
        instance = serializer.save()
        last_lesson = instance.lesson.last()
        if last_lesson:
            notify_subscribers_about_new_lesson.delay(last_lesson.id)
        send_mass_mailing.delay(
            "Обновление курса",
            "Курс был обновлён. Проверьте изменения.",
            [self.request.user.email]
        )


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


class StripePaymentAPIView(APIView):
    """
    Вьюшка для создания Stripe оплаты
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course_id = request.data.get("course_id")
        if not course_id:
            return Response({"error": "Не передан id курса"}, status=400)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Курс не найден"}, status=404)

        product = create_stripe_product(course.title)

        price = create_stripe_price(product.id, int(course.price))

        session = create_stripe_session(price.id)

        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            payment_method="card",
            payment_url=session.url,
        )

        return Response({"payment_url": session.url})
