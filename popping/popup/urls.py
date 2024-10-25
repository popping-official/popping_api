from django.urls import path

from .apis import user_follow_save_toggle, test_function_mongodb, user_follow_list_get
from .brand_apis import all_brand_data,brand_data, online_popup_store_main_data, BrandManagementAPI
from .product_api import product_data, CartAPI, cart_count_get
from .order_api import OrderApi

urlpatterns = [
    path('follow/toggle', user_follow_save_toggle, name='follow_toggle'),
    path('follow/list', user_follow_list_get, name='user_follow_list'),
    path('test', test_function_mongodb, name='follow_toggle'),


    path('brand', BrandManagementAPI.as_view(), name='brand_management'),
    path('brand/data', all_brand_data, name='all_brand_data'),
    path('brand/opening/<str:name>', brand_data, name='brands_opening'),
    path('brand/store/main/<str:name>', online_popup_store_main_data, name='brands_opening'),
    path('product/data/<str:brand>/<int:product>', product_data, name='product_data'),

    path('cart/data', CartAPI.as_view(), name='cart_data'),
    path('cart/count', cart_count_get, name='cart_data'),

    path('order', OrderApi.as_view(), name='cart_data'),
    ]