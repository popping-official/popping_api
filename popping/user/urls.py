from django.urls import path
from .apis import duplicate_check_api, SignUpAPI, UserAPI, signup_email_send_api, check_business_registration_api

urlpatterns = [
    path('duplicate/<str:option>', duplicate_check_api, name='duplicate'),
    path('business-registration', check_business_registration_api, name='check_business_registration_api'),
    path('signup/auth', signup_email_send_api, name='signup_email_send'),
    path('signup', SignUpAPI.as_view(), name='signup_api'),
    path('<str:uuid>', UserAPI.as_view(), name='user_api'),
]