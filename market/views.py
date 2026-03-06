from django.db.models import Q, F
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import StoreProfileForm, ItemForm, SignupForm
from django.contrib.auth import login

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
    if store.owner:
        return redirect("store_detail_username", username=store.owner.username)

    items = store.items.filter(is_available=True).order_by("-created_at")
    return render(request, "market/store_detail.html", {"store": store, "items": items})

def whatsapp_redirect(request, pk):
    item = get_object_or_404(Item, pk=pk, is_available=True)

    Item.objects.filter(pk=item.pk).update(whatsapp_clicks=F("whatsapp_clicks") + 1)

    whatsapp_link = item.whatsapp_url(request=request)
    return HttpResponseRedirect(whatsapp_link)

@login_required
def my_store(request):
    store = getattr(request.user, "store", None)

    if store is None:
        return render(request, "market/my_store_no_profile.html")

    items = store.items.order_by("-created_at")
    return render(request, "market/my_store.html", {"store": store, "items": items})

@login_required
def create_store_profile(request):
    if getattr(request.user, "store", None) is not None:
        return redirect("my_store")

    if request.method == "POST":
        form = StoreProfileForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.approved = True
            store.save()
            return redirect("my_store")
    else:
        form = StoreProfileForm()

    return render(request, "market/create_store_profile.html", {"form": form})

def _get_user_store(user):
    return getattr(user, "store", None)

@login_required
def item_create(request):
    store = _get_user_store(request.user)
    if store is None:
        return redirect("my_store")

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.store = store
            item.save()
            return redirect("my_store")
    else:
        form = ItemForm(initial={"is_available": True})

    return render(request, "market/item_form.html", {
        "form": form,
        "page_title": "Agregar producto",
        "submit_label": "Publicar producto",
    })

@login_required
def item_update(request, pk):
    store = _get_user_store(request.user)
    if store is None:
        return redirect("my_store")

    item = get_object_or_404(Item, pk=pk, store=store)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("my_store")
    else:
        form = ItemForm(instance=item)

    return render(request, "market/item_form.html", {
        "form": form,
        "page_title": "Editar producto",
        "submit_label": "Guardar cambios",
    })

@login_required
def item_delete(request, pk):
    store = _get_user_store(request.user)
    if store is None:
        return redirect("my_store")

    item = get_object_or_404(Item, pk=pk, store=store)

    if request.method == "POST":
        item.delete()
        return redirect("my_store")

    return render(request, "market/item_confirm_delete.html", {"item": item})

@login_required
def item_toggle_availability(request, pk):
    store = _get_user_store(request.user)
    if store is None:
        return redirect("my_store")

    item = get_object_or_404(Item, pk=pk, store=store)

    if request.method == "POST":
        item.is_available = not item.is_available
        item.save(update_fields=["is_available"])
    return redirect("my_store")

def signup(request):
    if request.user.is_authenticated:
        return redirect("my_store")

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("my_store")
    else:
        form = SignupForm()

    return render(request, "market/signup.html", {"form": form})

def store_detail_by_username(request, username):
    store = get_object_or_404(Store, owner__username=username, approved=True)
    items = store.items.filter(is_available=True).order_by("-created_at")
    return render(request, "market/store_detail.html", {"store": store, "items": items})

def store_directory(request):
    stores = Store.objects.filter(approved=True).select_related("owner").order_by("owner__username")

    return render(request, "market/store_directory.html"), {
        "stores": stores
    }
