
from datetime import time
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.schedulers import background
from myapp.management.commands.sendMessage import Command

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
