from django.contrib.auth.models import Group, Permission
from .models import Article, News


authors_group, _ = Group.objects.get_or_create(name='authors')


article_permissions = Permission.objects.filter(content_type__model='article')
authors_group.permissions.set(article_permissions)

news_permissions = Permission.objects.filter(content_type__model='news')
authors_group.permissions.set(news_permissions)