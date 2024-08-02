from django.urls import path
from .apis import duplicate_check_api, SignUpAPI

urlpatterns = [
    path('duplicate/<str:option>', duplicate_check_api, name='duplicate'),
    path('signup', SignUpAPI.as_view(), name='signup_api'),
]