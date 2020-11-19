from django.contrib import admin
from .models import Category, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug', 'sku', 'color', 'retail_price', 'whole_sale_price', 
	'available', 'created', 'updated']
	list_filter = ['available', 'color', 'created', 'updated']
	list_editable = ['retail_price', 'whole_sale_price', 'available']
	prepopulated_fields = {'slug': ('name',)}