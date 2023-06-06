from django import forms
from .models import News

from django import forms
from .models import Subscriber

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('category', 'email')

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'text', 'image')

class NewsDeleteForm(forms.Form):
    id = forms.IntegerField()

class NewsEditForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'text', 'image')

class ArticleForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'text', 'image')