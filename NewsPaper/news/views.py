from .forms import NewsForm
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from .filters import NewsFilter

from .models import Article
from .models import News
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect


from django.contrib.auth.mixins import PermissionRequiredMixin

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View
)
class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')

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



