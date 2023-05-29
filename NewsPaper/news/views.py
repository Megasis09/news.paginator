from django.shortcuts import render
from .models import News
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewsForm
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator

def news(request):
    all_news = News.objects.all()
    paginator = Paginator(all_news, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'news.html', context)


def search_news(request):
    if request.method == 'GET':
        q_title = request.GET.get('title', '')
        q_category = request.GET.get('category', '')
        q_date = request.GET.get('date', '')

        news_list = News.objects.filter(
            Q(title__icontains=q_title),
            Q(category__icontains=q_category),
            Q(pub_date__gte=q_date) if q_date else Q()
        ).order_by('-pub_date')

        context = {
            'news_list': news_list,
            'q_title': q_title,
            'q_category': q_category,
            'q_date': q_date,
        }
        return render(request, 'news/search.html', context)

def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news-list')
    else:
        form = NewsForm()
    return render(request, 'news/create_news.html', {'form': form})

def edit_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            return redirect('news-detail', pk=news_id)
    else:
        form = NewsForm(instance=news)
    return render(request, 'news/edit_news.html', {'form': form, 'news': news})

def delete_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    news.delete()
    return redirect('news-list')

def news_list_view(request):
    news_list = News.objects.order_by('-published_date')
    context = {
        'news_list': news_list,
    }
    return render(request, 'news_list.html', context)

def news_detail_view(request, pk):
    news = News.objects.get(pk=pk)
    context = {
        'news': news,
    }
    return render(request, 'news_detail.html', context)


