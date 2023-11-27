from django.urls import path, include

app_name = 'api_v1'

urlpatterns = [
    path('users/', include('apps.api_v1.urls.user_urls')),
]
