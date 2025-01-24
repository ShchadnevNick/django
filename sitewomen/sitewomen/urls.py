from django.urls import path, include
from women.views import page_not_found


handler404 = page_not_found

urlpatterns = [
    path('', include('women.urls')),
]
