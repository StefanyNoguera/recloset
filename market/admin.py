from django.contrib import admin
from .models import Store, Item


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("handle", "city", "whatsapp_number", "approved", "total_whatsapp_clicks", "created_at")
    list_filter = ("approved", "city")
    search_fields = ("owner__username", "city", "whatsapp_number", "instagram_handle")

    @admin.display(description="Tienda")
    def handle(self, obj):
        return f"@{obj.owner.username}" if obj.owner else "(sin usuario)"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "store", "price_cop", "size", "category", "condition", "is_available", "whatsapp_clicks", "created_at")
    list_filter = ("category", "condition", "is_available", "store")
    search_fields = ("title", "description", "store__owner__username")
