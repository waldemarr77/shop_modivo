from celery import shared_task
from .models import Order
from django.utils import timezone
from datetime import timedelta


@shared_task
def canceled_pending_orders():
    deadline = timezone.now() - timedelta(hours=24)

    Order.objects.filter(status='pending', created_at__lt=deadline).update(status='cancelled')
