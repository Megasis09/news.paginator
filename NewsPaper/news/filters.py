from django import template

from django_filters import FilterSet, DateTimeFilter, CharFilter, ChoiceFilter
from django.forms import DateTimeInput

register = template.Library()

@register.filter
def censor(value):
    censored_words = ['bad_word1', 'bad_word2', 'bad_word3']
    for word in censored_words:
        value = value.replace(word, '*' * len(word))
    return value


class NewsFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    category = ChoiceFilter(field_name='category', choices=News.CATEGORIES)
    published_after = DateTimeFilter(
    field_name='published_at',
    lookup_expr='gt',
    widget=DateTimeInput(
    format='%Y-%m-%dT%H:%M',
    attrs={'type': 'datetime-local'},
    ),
    )

    class Meta:
        model = News
        fields = {
            'title': ['icontains'],
            'tag': ['icontains'],
        }