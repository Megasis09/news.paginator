

from django.apps import AppConfig
from django.contrib.auth.models import Group, Permission




class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
