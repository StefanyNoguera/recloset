from django.shortcuts import render
from .models import Item

def home(request):
    items = Item.objects.filter(is_available=True).order_by("-created_at")
    return render(request, "market/home.html", {"items": items})
