from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist_view, name='wishlist'),
    path('api/add/<str:id_product>', views.wishlist_add_json, name='wishlist_add'),
    path('api/del/<str:id_product>', views.wishlist_del_json, name='wishlist_del'),
    path('api/', views.wishlist_json, name='wishlist_json'),
]