from django.urls import path
from . import views

app_name = 'users'  # Пространство имен приложения

urlpatterns = [
    # Полное имя:'users:login'
    path('login/', views.login_user, name='login'),
    # Полное имя:'users:logout'
    path('logout/', views.logout_user, name='logout'),
]
