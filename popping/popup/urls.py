from django.urls import path

from .apis import user_follow_save_toggle, test_function_mongodb
from .brand_apis import brand_data, online_popup_store_main_data
from .product_api import product_data

urlpatterns = [
    path('follow/toggle', user_follow_save_toggle, name='follow_toggle'),
    path('test', test_function_mongodb, name='follow_toggle'),
    path('brand/opening/<str:name>', brand_data, name='brands_opening'),
    path('brand/store/main/<str:name>', online_popup_store_main_data, name='brands_opening'),
    path('product/data/<str:brand>/<int:product>', product_data, name='product_data'),
    ]