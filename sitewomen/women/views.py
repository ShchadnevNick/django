from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse('<h1>Главая страница</h1>')

def about(request):
    return HttpResponse('О сайте')
