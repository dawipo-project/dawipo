from django import forms
from django.contrib.auth.models import User
from .models import Category, Product

# Formulario de autenticación de usuarios
class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'sku', 'image', 'description', 'color',
            'measures', 'retail_price', 'whole_sale_price',
            'available')

class ProductCreateForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ('name', 'sku', 'image', 'description', 'color', 
			'measures', 'retail_price', 'whole_sale_price', 'available')

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		exclude = ('company',)