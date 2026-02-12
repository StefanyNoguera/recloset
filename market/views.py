from django.shortcuts import render, get_object_or_404
from .models import Item

def home(request):
    items = Item.objects.filter(is_available=True).order_by("-created_at")
    return render(request, "market/home.html", {"items": items})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk, is_available=True)
    whatsapp_link = item.whatsapp_url(request=request)
    return render(request, "market/item_detail.html", {"item": item, "whatsapp_link": whatsapp_link})
