from django import forms
from .models import Store, Item, User
from django.contrib.auth.forms import UserCreationForm

class StoreProfileForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ["city", "whatsapp_number", "instagram_handle"]
        labels = {
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
    extra_photos = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"multiple": True}),
        label="Fotos adicionales",
        help_text="Puedes subir varias fotos al mismo tiempo."
    )

    class Meta:
        model = Item
        fields = ["title", "description", "price_cop", "size", "category", "condition", "photo", "is_available"]
        labels = {
            "title": "Título",
            "description": "Descripción (opcional)",
            "price_cop": "Precio (COP)",
            "size": "Talla",
            "category": "Categoría",
            "condition": "Condición",
            "photo": "Foto principal",
            "is_available": "Disponible",
        }
        help_texts = {
            "price_cop": "Solo números. Ej: 45000",
            "size": "Ej: S, M, L, 28, 40, Única",
            "photo": "Esta será la primera foto que verá la gente.",
        }
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900",
                "rows": 3
            }),
            "price_cop": forms.NumberInput(attrs={
                "class": "w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            }),
            "size": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            }),
            "category": forms.Select(attrs={
                "class": "w-full rounded-xl border border-gray-300 px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-gray-900"
            }),
            "condition": forms.Select(attrs={
                "class": "w-full rounded-xl border border-gray-300 px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-gray-900"
            }),
            "photo": forms.ClearableFileInput(attrs={
                "class": "w-full text-sm"
            }),
            "is_available": forms.CheckboxInput(attrs={
                "class": "h-4 w-4"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["extra_photos"].widget.attrs.update({
            "class": "w-full text-sm"
        })

    def clean_extra_photos(self):
        files = self.files.getlist("extra_photos")
        if len(files) > 4:
            raise forms.ValidationError("Puedes subir máximo 4 fotos adicionales.")
        return files

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].label = "Usuario"
        self.fields["password1"].label = "Contraseña"
        self.fields["password2"].label = "Confirmar contraseña"

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full rounded-xl border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-gray-900"
            })
