# map/urls.py
from django.urls import path
from .apis import list_maps, pd_test

urlpatterns = [
    # path('geo-addr/<str:addr>', geocode_addr, name='duplicate'),
    path('list', list_maps, name='map-list'),
    
    path('test', pd_test, name='test'),
]