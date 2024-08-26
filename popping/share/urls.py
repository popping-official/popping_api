# map/urls.py
from django.urls import path
from .apis import GridFSImageView

urlpatterns = [
    path('grid-image', GridFSImageView.as_view(), name='grid-image'),
]