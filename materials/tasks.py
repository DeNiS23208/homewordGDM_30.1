from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import Lesson

@shared_task
def notify_subscribers_about_new_lesson(lesson_id):
    try:
        lesson = Lesson.objects.get(id=lesson_id)
        course = lesson.course

        # Проверка: обновлялся ли курс за последние 4 часа
        if course.updated_at and timezone.now() - course.updated_at < timedelta(hours=4):
            return

        course.updated_at = timezone.now()
        course.save()

        # Рассылка подписчикам
        for sub in course.subscriptions.all():
            send_mail(
                subject=f'Обновление курса {course.title}',
                message=f'Добавлен урок: {lesson.title}',
                from_email='noreply@example.com',
                recipient_list=[sub.user.email],
                fail_silently=True,
            )

    except Lesson.DoesNotExist:
        print(f"[ERROR] Lesson with ID {lesson_id} не найден.")