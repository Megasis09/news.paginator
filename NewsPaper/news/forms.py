from django import forms
from .models import News

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