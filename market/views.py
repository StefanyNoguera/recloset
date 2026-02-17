from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Item, Store

def home(request):
    items = (
        Item.objects
        .filter(is_available=True, store__approved=True)
        .select_related("store")
        .order_by("-created_at")
    )

    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    condition = request.GET.get("condition", "").strip()
    size = request.GET.get("size", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()

    if q:
        items = items.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(store__name__icontains=q)
        )

    if category:
        items = items.filter(category=category)

    if condition:
        items = items.filter(condition=condition)

    if size:
        items = items.filter(size__iexact=size)

    if min_price.isdigit():
        items = items.filter(price__gte=int(min_price))

    if max_price.isdigit():
        items = items.filter(price__lte=int(max_price))

    context = {
        "items": items,
        "q": q,
        "category": category,
        "condition": condition,
        "size": size,
        "min_price": min_price,
        "max_price": max_price,
        "category_choices": Item.Category.choices,
        "condition_choices": Item.Condition.choices,
    }

    return render(request, "market/home.html", context)


def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk, is_available=True)
    whatsapp_link = item.whatsapp_url(request=request)
    return render(request, "market/item_detail.html", {"item": item, "whatsapp_link": whatsapp_link})

def store_detail(request, pk):
    store = get_object_or_404(Store, pk=pk, approved=True)
    items = store.items.filter(is_available=True).order_by("-created_at")
    return render(request, "market/store_detail.html", {"store": store, "items": items})
