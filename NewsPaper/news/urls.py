from .views import news_list_view, news_detail_view
from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from .management.commands.runapscheduler import Command
from news.views import CategoryListView, subscribe

urlpatterns = [
    path('create/', views.create_news, name='create-news'),
    path('news/', news_list_view, name='news_list'),
    path('news/<int:pk>/', news_detail_view, name='news_detail'),
    path('<int:pk>/edit/', views.edit_news, name='edit-news'),
    path('<int:pk>/delete/', views.delete_news, name='delete-news'),
    path('create/', views.create_article, name='create-article'),
    path('<int:pk>/edit/', views.edit_article, name='edit-article'),
    path('<int:pk>/delete/', views.delete_article, name='delete-article'),
    path('', views.index, name='index'),
    path('news/search/', views.search_news, name='search'),
    path('details/<int:news_id>/', views.details, name='details'),
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('news/', include('simpleapp.urls')),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
]

try:
    command = Command()
    command.handle()
except Exception as e:
    logging.exception("Failed to start APScheduler: %s" % e)

