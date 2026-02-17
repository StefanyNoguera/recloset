from django.urls import path
from .views import home, item_detail, store_detail

urlpatterns = [
    path("", home, name="home"),
    path("productos/<int:pk>/", item_detail, name="item_detail"),
    path("tiendas/<int:pk>/", store_detail, name="store_detail")
]
