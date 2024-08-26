from django.urls import path
from .apis import signin_api, signout_api, duplicate_check_api, SignUpAPI, UserAPI, signup_email_send_api, check_business_registration_api, UserManagementAPI, MyPageAPI, AddressAPI, grade_point_info_api,\
    AccountChangeAPI
from .social_auth import social_login

urlpatterns = [
    path('', UserAPI.as_view(), name='user_api'),
    path('signin', signin_api, name='signin_api'),
    path('signout', signout_api, name='signout_api'),
    path('signup', SignUpAPI.as_view(), name='signup_api'),
    path('email/auth', signup_email_send_api, name='signup_email_send'),
    path('duplicate/<str:option>', duplicate_check_api, name='duplicate'),
    path('business-registration', check_business_registration_api, name='check_business_registration_api'),
    path('retrieve/<str:option>', UserManagementAPI.as_view(), name='user_management_api'),
    path('social/auth/<str:provider>', social_login, name='social_login'),
    path('mypage', MyPageAPI.as_view(), name='mypage'),
    path('benefit', grade_point_info_api, name='grade_point_info_api'),
    path('address', AddressAPI.as_view(), name='address'),
    path('change', AccountChangeAPI.as_view(), name='change'),
]
