from django import forms
from django.contrib.auth.models import User
from .models import Category, Product

# Formulario de autenticación de usuarios
class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'sku', 'image', 'description', 
        	'observations', 'brand', 'color', 'provider', 
            'price_1', 'price_2', 'price_3', 'barcode', 'measures',
            'fabrication_cost', 'tax', 'available')
        price_1 = forms.DecimalField(decimal_places=2, localize=True, blank=True)
        price_2 = forms.DecimalField(decimal_places=2, localize=True, blank=True)
        price_3 = forms.DecimalField(decimal_places=2, localize=True, blank=True)
        fabrication_cost = forms.DecimalField(decimal_places=2, localize=True, blank=True)
        tax = forms.DecimalField(decimal_places=2, localize=True, blank=True)

class ProductCreateForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ('category', 'name', 'sku', 'image', 'description', 
            'observations', 'brand', 'color', 'provider', 
            'price_1', 'price_2', 'price_3', 'barcode', 'measures',
            'fabrication_cost', 'tax', 'available')
        price_1 = forms.DecimalField(decimal_places=2, localize=True, blank=True)
        price_2 = forms.DecimalField(decimal_places=2, localize=True, blank=True)
        price_3 = forms.DecimalField(decimal_places=2, localize=True, blank=True)
        fabrication_cost = forms.DecimalField(decimal_places=2, localize=True, blank=True)
        tax = forms.DecimalField(decimal_places=2, localize=True, blank=True)

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		exclude = ('company',)