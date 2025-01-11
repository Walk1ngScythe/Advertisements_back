from django.forms import ModelForm
from .models import Bb
from django import forms

class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Поиск по названию')
