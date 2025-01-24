from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse('<h1>Главая страница</h1>')

def about(request):
    return HttpResponse('О сайте')

def categories(request, cat_slug):
    return HttpResponse(f'Страница с категорией: {cat_slug}')

def archive(request, year):
    return HttpResponse(f'<h2>Страница с архивом {year} года</h2>')