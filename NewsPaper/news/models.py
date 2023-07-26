from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters import FilterSet, DateTimeFilter, CharFilter, ChoiceFilter
from django.forms import DateTimeInput


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

class Subscriber(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

@receiver(post_save, sender=News)
def send_notification(sender, instance, **kwargs):
    subject = 'New news: {0}'.format(instance.title)
    message = 'Check out the latest news on our website!\n\n{0}'.format(instance.get_absolute_url())
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [subscriber.email for subscriber in Subscriber.objects.all()]
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)




class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')
    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:20] + '...'

class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f' {self.post.title} | {self.category.name}'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def get_news(self):
        from . import News
        return News.objects.filter(article=self)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)


        cache.delete(f'article_{self.id}')

    def get_from_cache(self):
        article = cache.get(f'article_{self.id}')
        if article is None:

            article = Article.objects.get(id=self.id)


            cache.set(f'article_{self.id}', article, settings.CACHE_TIMEOUT)

        return article

class News(models.Model):
    def init(self, title, author, content, timestamp):
        self.title = title
        self.author = author
        self.content = content
        self.timestamp = timestamp

        def get_title(self):
            return self.title

        def get_author(self):
            return self.author

        def get_content(self):
            return self.content

        def get_timestamp(self):
            return self.timestamp

        def set_title(self, title):
            self.title = title

        def set_author(self, author):
            self.author = author

        def set_content(self, content):
            self.content = content

        def set_timestamp(self, timestamp):
            self.timestamp = timestamp

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {"username": UsernameField}





