from django.contrib import admin
from .models import Store, Item
# Register your models here.

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "whatsapp_number", "approved", "total_whatsapp_clicks", "created_at")
    list_filter = ("approved", "city")
    search_fields = ("name", "city", "whatsapp_number", "instagram_handle")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "store", "price", "size", "category", "condition", "is_available", "whatsapp_clicks", "created_at")
    list_filter = ("category", "condition", "is_available", "store")
    search_fields = ("title", "description", "store__name")
