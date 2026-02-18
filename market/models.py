from django.db import models
from django.db.models import Sum

class Store(models.Model):
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=80)
    whatsapp_number = models.CharField(
        max_length=20,
        help_text="Use dolo digitos, incluya prefijo internacional. Ejemplo: 573001234567"
    )
    instagram_handle = models.CharField(max_length=50)
    approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def total_whatsapp_clicks(self):
        total = self.items.aggregate(total=Sum("whatsapp_clicks"))["total"]
        return total or 0


class Item(models.Model):
    class Category(models.TextChoices):
        TOPS = "tops", "Blusas / Tops"
        BOTTOMS = "bottoms", "Pantalones / Faldas"
        DRESSES = "dresses", "Vestidos"
        OUTERWEAR = "outerwear", "Chaquetas / Abrigos"
        SHOES = "shoes", "Zapatos"
        ACCESSORIES = "accessories", "Accesorios"
        OTHER = "other", "Otro"

    class Condition(models.TextChoices):
        NEW = "new", "Nuevo"
        LIKE_NEW = "like_new", "Como nuevo"
        GOOD = "good", "Buena"
        FAIR = "fair", "Aceptable"

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="items")

    title = models.CharField(max_length=140)
    description = models.TextField()

    price = models.PositiveIntegerField(help_text="Precio en pesos colombianos, no puntos/comas")
    size = models.CharField(max_length=20, help_text="Ejemplo: S, M, L, 28, 40, Única")
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    condition = models.CharField(max_length=20, choices=Condition.choices, default=Condition.GOOD)

    photo = models.ImageField(upload_to="items/")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    whatsapp_clicks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} — {self.store.name}"

    def whatsapp_url(self, request=None):
        import urllib.parse

        phone = "".join(filter(str.isdigit, self.store.whatsapp_number))

        item_url = ""
        if request is not None:
            item_url = request.build_absolute_uri()

        text = f"Hola! Vi este artículo en Recloset: {self.title}. ¿Está disponible? {item_url}".strip()
        return f"https://wa.me/{phone}?text={urllib.parse.quote(text)}"
