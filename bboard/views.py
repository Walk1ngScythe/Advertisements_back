from django.views.generic.edit import CreateView
from .forms import BbForm, SearchForm
from .models import Bb, Rubric
from django.shortcuts import render
from django.urls import reverse_lazy


def index(request):
    bbs = Bb.objects.all()  # По умолчанию показываем все объявления
    rubrics = Rubric.objects.all()
    query = request.GET.get('query', '')  # Получаем текст для поиска из параметров GET

    if query:
        # Если есть запрос, фильтруем объявления по названию
        bbs = bbs.filter(title__icontains=query)

    context = {
        'bbs': bbs,
        'rubrics': rubrics,
        'query': query,  # Передаем текст поискового запроса
    }

    return render(request, 'bboard/index.html', context)

def rubric_bbs(request, rubric_id):
    bbs = Bb.objects.filter(rubric_id=rubric_id)  # Фильтруем по рубрике
    rubrics = Rubric.objects.all()
    query = request.GET.get('query', '')  # Получаем текст для поиска из параметров GET

    if query:
        # Если есть запрос, фильтруем объявления по названию в выбранной рубрике
        bbs = bbs.filter(title__icontains=query)

    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {
        'bbs': bbs,
        'rubrics': rubrics,
        'current_rubric': current_rubric,  # Передаем текущую рубрику
        'query': query,  # Передаем текст поискового запроса
    }
    return render(request, 'bboard/rubric_bbs.html', context)

class BbCreateView(CreateView):
    template_name = 'bboard/bb_create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context