
from datetime import time
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.schedulers import background
from myapp.management.commands.sendMessage import Command

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from .models import News, Subscriber

@shared_task
def send_newsletter():
    week_ago = datetime.now() - timedelta(days=7)
    latest_news = News.objects.filter(pub_date__gte=week_ago)
    subject = 'Последние новости с нашего сайта'
    message = 'Следите за последними новостями на нашем сайте:\n\n{0}'.format('\n\n'.join(news.get_absolute_url() for news in latest_news))
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [subscriber.email for subscriber in Subscriber.objects.all()]
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)

scheduler = background.BackgroundScheduler(timezone="UTC")
scheduler.add_jobstore(DjangoJobStore(), "default")

scheduler.add_job(
    Command().handle,
    trigger="cron",
    day_of_week="fri",
    hour=18,
    minute=0,
    second=0,
    id="send_message_job",
)

scheduler.start()
