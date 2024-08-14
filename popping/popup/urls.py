from django.urls import path
from .apis import user_follow_save_toggle, test_function_mongodb

urlpatterns = [
    path('follow/toggle', user_follow_save_toggle, name='follow_toggle'),
    path('test', test_function_mongodb, name='follow_toggle'),
    ]