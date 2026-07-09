from celery import shared_task
import time

@shared_task(bind=True, max_retries=3)
def send_welcome_email(self, user_email):
    try:
        time.sleep(5) 
        print(f"✅ Успішно відправлено Email на адресу: {user_email}")
        return "Email sent!"
    except Exception as exc:
        self.retry(exc=exc, countdown=10)