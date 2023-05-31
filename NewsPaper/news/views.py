from .forms import NewsForm
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from .filters import NewsFilter

from .models import Article

from django.utils.translation import reverse_lazy

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from .models import News

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

class NewsList(ListView):
    model = News
    ordering = 'name'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = News
    template_name = 'news.html'
    context_object_name = 'News'


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_news',)
    form_class = NewsForm
    model = News
    template_name = 'edit_news.html'


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.change_news',)
    form_class = NewsForm
    model = News
    template_name = 'edit_news.html'


class ProductDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.delete_news',)
    model = News
    template_name = 'delete_news.html'
    success_url = reverse_lazy('news_list')

class ArticleList(ListView):
    model = Article
    ordering = 'name'
    template_name = 'news.html'
    context_object_name = 'article'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticleDetail(DetailView):
    model = Article
    template_name = 'news.html'
    context_object_name = 'Article'


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_article',)
    form_class = NewsForm
    model = Article
    template_name = 'edit_article.html'


class ProductUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.change_product',)
    form_class = NewsForm
    model = News
    template_name = 'edit_news.html'


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.delete_article',)
    model = Article
    template_name = 'delete_article.html'
    success_url = reverse_lazy('article_list')



