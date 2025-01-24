from django.urls import path
from women import views


urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='home'),
]