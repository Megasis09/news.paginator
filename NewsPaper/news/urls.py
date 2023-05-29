from .views import news_list_view, news_detail_view
from django.urls import path
from . import views

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
    path('news/search/', search, name='search'),
    path('details/<int:news_id>/', views.details, name='details'),
]

