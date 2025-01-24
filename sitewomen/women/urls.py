from django.urls import path, re_path
from women import views


urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('cats/<slug:cat_slug>', views.categories, name='cats'),
    re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive, name='archive')
]