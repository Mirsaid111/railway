from celery import shared_task
from django.core.mail import send_mail
import time

@shared_task
def send_weekly_report():
    # Логика отправки отчета
    send_mail(
        'Еженедельный отчет MedBook',
        'Ваша статистика за неделю...',
        'noreply@medbook.com',
        ['user@example.com'],
        fail_silently=False,
    )

def example_task(duration):
    time.sleep(duration)
    return f"Task completed after {duration} seconds"