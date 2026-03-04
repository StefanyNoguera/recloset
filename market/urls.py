from django.urls import path
from .views import home, item_detail, store_detail, whatsapp_redirect, my_store, create_store_profile, item_create, item_update, item_delete, item_toggle_availability, signup

urlpatterns = [
    path("", home, name="home"),
    path("productos/<int:pk>/", item_detail, name="item_detail"),
    path("productos/<int:pk>/whatsapp", whatsapp_redirect, name="whatsapp_redirect"),
    path("tiendas/<int:pk>/", store_detail, name="store_detail"),
    path("mi-tienda/", my_store, name="my_store"),
    path("mi-tienda/crear-perfil/", create_store_profile, name="create_store_profile"),
    path("mi-tienda/productos/nuevo/", item_create, name="item_create"),
    path("mi-tienda/productos/<int:pk>/editar/", item_update, name="item_update"),
    path("mi-tienda/productos/<int:pk>/eliminar/", item_delete, name="item_delete"),
    path("mi-tienda/productos/<int:pk>/toggle-disponible/", item_toggle_availability, name="item_toggle_availability"),
    path("crear-cuenta/", signup, name="signup"),
]
