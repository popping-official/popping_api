from django.urls import path
from .apis import user_follow_save_toggle

urlpatterns = [
    path('follow/toggle', user_follow_save_toggle, name='follow_toggle'),
]