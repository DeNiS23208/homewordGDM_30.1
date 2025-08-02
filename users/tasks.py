from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

@shared_task
def deactivate_inactive_users():
    cutoff = timezone.now() - timedelta(days=30)
    users = User.objects.filter(last_login__lt=cutoff, is_active=True)
    count = users.update(is_active=False)
    print(f'Деактивировано пользователей: {count}')

@shared_task
def send_mass_mailing(subject, message, recipients):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipients,
        fail_silently=False
    )