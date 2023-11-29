from django.urls import path, include

from apps.api.spectacular.urls import urlpatterns as doc_urls
from apps.api_v1.urls.core_urls import urlpatterns as user_urls
from apps.core.urls import urlpatterns as core_urls

app_name = "api"

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_urls
urlpatterns += user_urls
urlpatterns += core_urls

