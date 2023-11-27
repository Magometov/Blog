from django.urls import path, include

from apps.api.spectacular.urls import urlpatterns as doc_urls

app_name = "api"

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urls

