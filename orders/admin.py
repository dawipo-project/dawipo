from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem, OrderChange, OrderStatus, PaymentMethod

# Register your models here.
class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ['product']

def order_detail(obj):
	url = reverse('orders:admin_order_detail', args=[obj.id])
	return mark_safe(f'<a href="{url}">View</a>')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'customer', 'status',
	'created', 'updated', order_detail]
	list_filter = ['status', 'created', 'updated']
	inlines = [OrderItemInline]

@admin.register(OrderChange)
class OrderChangeAdmin(admin.ModelAdmin):
	list_display = ['id', 'order', 'change', 'date']

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
	list_display = ['name', 'es_name']
	prepopulated_fields = {'slug': ('name',)}

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
	list_display = ['name']