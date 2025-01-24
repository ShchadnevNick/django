from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render

def index(request):
    return HttpResponse('<h1>Главая страница</h1>')

def about(request):
    return HttpResponse('О сайте')

def categories(request, cat_slug):
    return HttpResponse(f'Страница с категорией: {cat_slug}')

def archive(request, year):
    if year > 2025:
        raise Http404()
    return HttpResponse(f'<h2>Страница с архивом {year} года</h2>')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1> <h2>У вас ошибка</h2>")