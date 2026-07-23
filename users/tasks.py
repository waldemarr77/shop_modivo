from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task(bind=True, max_retries=3)
def send_welcome_email(self, user_email):
    try:
        send_mail(
            subject='Вітаємо у Shop Modivo!',
            message='Дякуємо за реєстрацію на нашому сайті. Вдалих покупок!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            fail_silently=False,
        )
        return "Email sent!"
    except Exception as exc:
        self.retry(exc=exc, countdown=10)