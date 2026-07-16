from celery import shared_task
from .models import Order
from django.utils import timezone
from datetime import timedelta


@shared_task
def canceled_pending_orders():
    deadline = timezone.now() - timedelta(hours=24)

    Order.objects.filter(status='pending', created_at__lt=deadline).update(status='cancelled')


@shared_task(bind=True, max_retries=3)
def send_order_confirmation(self, order_id, user_email):
    try:
        print(f'Замовлення №{order_id} підтверджено та відправлено на {user_email}')
    except Exception as exc:
        self.retry(exc=exc, countdown=10)
