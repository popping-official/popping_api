# map/urls.py
from django.urls import path
from .apis import store_list, daco_crawling, geo_addr, surround_place

urlpatterns = [
    # path('geo-addr/<str:addr>', geocode_addr, name='duplicate'),
    path('crawling', daco_crawling, name='crawling'),
    path('geocode', geo_addr, name='geo_addr'),
    path('stores', store_list, name='map-list'),
    path('surround/<str:option>', surround_place, name='surround'),
]