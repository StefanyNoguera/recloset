from django.urls import path
from .views import home, item_detail, store_detail, whatsapp_redirect, my_store

urlpatterns = [
    path("", home, name="home"),
    path("productos/<int:pk>/", item_detail, name="item_detail"),
    path("productos/<int:pk>/whatsapp", whatsapp_redirect, name="whatsapp_redirect"),
    path("tiendas/<int:pk>/", store_detail, name="store_detail"),
    path("mi-tienda/", my_store, name="my_store"),
]
