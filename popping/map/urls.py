# map/urls.py
from django.urls import path
from .apis import surround_place, offline_popups, popup_detail, count_view, surround_popup, main_popup

urlpatterns = [
    path('main-popups', main_popup, name='main-popups'),
    path('off-popups', offline_popups, name='off-popup'),
    path('popup/<str:popupId>', popup_detail, name='popup'),
    path('surround-place', surround_place, name='surround-place'),
    path('surround-popup', surround_popup, name='surround-popup'),
    path('view-count/<str:popupId>', count_view, name='view-count'),
]