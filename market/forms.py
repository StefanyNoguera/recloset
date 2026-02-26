from django import forms
from .models import Store, Item

class StoreProfileForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ["name", "city", "whatsapp_number", "instagram_handle"]
        labels = {
            "name": "Nombre de la tienda",
            "city": "Ciudad",
            "whatsapp_number": "Número de Whatsapp",
            "instagram_handle": "Usuario de Instagram"
        }
        help_texts = {
            "whatsapp_number": "Solo dígitos, con código de país. Ej: 573001234567",
            "instagram_handle": "Sin @. Ej: recloset_co"
        }

    def clean_whatsapp_number(self):
        value = self.cleaned_data["whatsapp_number"].strip()
        if not value.isdigit():
            raise forms.ValidationError("El número de WhatsApp debe contener solo dígitos.")
        if len(value) < 11:
            raise forms.ValidationError("El número parece muy corto. Revisa que esté completo.")
        return value

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["title", "description", "price", "size", "category", "condition", "photo", "is_available"]
        labels = {
            "title": "Título",
            "description": "Descripción (opcional)",
            "price_cop": "Precio (COP)",
            "size": "Talla",
            "category": "Categoría",
            "condition": "Condición",
            "photo": "Foto",
            "is_available": "Disponible",
        }

        help_texts = {
            "price_cop": "Solo números. Ej: 45000",
            "size": "Ej: S, M, L, 28, 40, Única",
        }
