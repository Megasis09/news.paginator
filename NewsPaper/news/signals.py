from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Article
from .models import Subscriber
@receiver(post_save, sender=Article)
def send_email_to_subscribers(sender, instance, **kwargs):
    subscribers = Subscriber.objects.filter(category=instance.category)
    for subscriber in subscribers:
        subject = 'Новая статья в ' + instance.category
        message = 'Дорогой ' + subscriber.user.username + ',\n\n' + 'Мы только что опубликовали новую статью в категории ' + instance.category + '.' + '\n\n Пожалуйста, перейдите по ссылке https://127.0.0.1:8000/articles/' + str(instance.id) + ' прочитать статью.'