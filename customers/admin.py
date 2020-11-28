from django.contrib import admin
from.models import Customer, CustomerContact

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ['name', 'city', 'first_name', 'last_name', 'email']
	list_filter = ['name', 'city']

@admin.register(CustomerContact)
class CustContactAdmin(admin.ModelAdmin):
	list_display = ['contact', 'company']
	list_filter = ['company']