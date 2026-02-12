from django.db import models

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

class Item(models.Model):
    class Category(models.TextChoices):
        TOPS = "tops", "Tops"
        BOTTOMS = "bottoms", "Bottoms"
        DRESSES = "dresses", "Dresses"
        OUTERWEAR = "outerwear", "Outerwear"
        SHOES = "shoes", "Shoes"
        ACCESSORIES = "accessories", "Accessories"
        OTHER = "other", "Other"

    class Condition(models.TextChoices):
        NEW = "new", "New"
        LIKE_NEW = "like_new", "Like new"
        GOOD = "good", "Good"
        FAIR = "fair", "Fair"

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

    def __str__(self):
        return f"{self.title} — {self.store.name}"
