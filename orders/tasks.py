from celery import shared_task
from .models import Order
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def canceled_pending_orders():
    deadline = timezone.now() - timedelta(hours=24)

    Order.objects.filter(status='pending', created_at__lt=deadline).update(status='cancelled')


@shared_task(bind=True, max_retries=3)
def send_order_confirmation(self, order_id, user_email):
    try:
        send_mail(
            subject=f'Підтвердження замовлення №{order_id}',
            message=f'Ваше замовлення №{order_id} успішно оплачено та передано в обробку.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            fail_silently=False,
        )
    except Exception as exc:
        self.retry(exc=exc, countdown=10)
