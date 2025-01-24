from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.urls import reverse


def index(request):
    return HttpResponse('<h1>Главая страница</h1>')

def about(request):
    return HttpResponse('О сайте')

def categories(request, cat_slug):
    return HttpResponse(f'Страница с категорией: {cat_slug}')

def archive(request, year):
    if year > 2025:
        url_redirect = reverse('cats', args=('music',))
        return HttpResponsePermanentRedirect(url_redirect)

    return HttpResponse(f'<h1>Архив по годам </h1> <h2>{year}</h2>')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1> <h2>У вас ошибка</h2>")