from django.urls import path

from apps.api_v1.views.user_view import (
    send_user_data,
    send_password,
    user_registration,
)

urlpatterns = [
    path('send_first_data/', send_user_data),
    path('send_password/', send_password),
    path('registration/', user_registration),
]
