from .forms import NewsForm
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from .filters import NewsFilter
from .forms import SubscriptionForm
from .models import Subscriber
from .models import Article, News, Post, Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View
)

from django.db import models
from django.contrib.auth.models import User

class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')

class CategoryListView(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_new_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date')
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context
@user_passes_test(lambda u: u.groups.filter(name='authors').exists())
def edit_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':

    return render(request, 'edit_news.html', {'news': news})

@user_passes_test(lambda u: u.groups.filter(name='authors').exists())
def create_article(request):
    if request.method == 'POST':

    return render(request, 'create_article.html')

def news(request):
    all_news = News.objects.all()
    paginator = Paginator(all_news, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'news.html', context)


def search(request):
    query = request.GET.get('q')
    results = News.objects.filter(Q(title__contains=query) | Q(tags__contains=query) | Q(date__contains=query))
    context = {'results': results}
    return render(request, 'search.html', context)

class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Article
    fields = ['title', 'content']


    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()


    def get_success_url(self):
        return reverse('article_list')


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'content']


    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()


    def get_success_url(self):
        return reverse('article_list')


class NewsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = News
    fields = ['title', 'content']


    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()


    def get_success_url(self):
        return reverse('news_list')


class NewsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    fields = ['title', 'content']


    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()


    def get_success_url(self):
        return reverse('news_list')


@login_required
def subscriptions(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscriber = form.save(commit=False)
            subscriber.user = request.user
            subscriber.save()
            return redirect('subscriptions')
    else:
        form = SubscriptionForm()
        subscriptions = Subscriber.objects.filter(user=request.user)
        return render(request, 'subscriptions.html', {'form': form, 'subscriptions': subscriptions})
