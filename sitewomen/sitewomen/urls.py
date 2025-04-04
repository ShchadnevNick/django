from django.conf.urls.static import static
from sitewomen import settings
from django.urls import path, include
from women.views import page_not_found
from django.contrib import admin



handler404 = page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG: # Проверяется, включен ли DEBUG-режим
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Панель администрирования'
admin.site.index_title = "Известные женщины мира"


