from django.contrib import admin
from .models import Order, OrderItem, OrderChange, OrderStatus

# Register your models here.
class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'customer', 'status',
	'created', 'updated']
	list_filter = ['status', 'created', 'updated']
	inlines = [OrderItemInline]

@admin.register(OrderChange)
class OrderChangeAdmin(admin.ModelAdmin):
	list_display = ['id', 'order', 'change', 'date']

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
	list_display = ['name', 'es_name']