from django import forms
from django.contrib.auth.models import User
from .models import Category, Product

# Formulario de autenticación de usuarios
class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'sku', 'image', 'description', 
        	'observations', 'price_1', 'price_2', 'price_3',
            'fabrication_cost', 'tax', 'available')

class ProductCreateForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ('name', 'sku', 'image', 'description', 
        	'observations', 'price_1', 'price_2', 'price_3',
            'fabrication_cost', 'tax', 'available')

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		exclude = ('company',)