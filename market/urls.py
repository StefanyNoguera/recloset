from django.urls import path
from .views import home, item_detail

urlpatterns = [
    path("", home, name="home"),
    path("items/<int:pk>/", item_detail, name="item_detail")
]
