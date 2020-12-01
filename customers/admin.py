from django.contrib import admin
from.models import Customer, CustomerContact, DocumentType, Regime, PersonType

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
	list_display = ['name', 'city', 'first_name', 'last_name', 'email',
	'document', 'regime', 'person_type', 'cust_contact']
	list_filter = ['name', 'city']

@admin.register(CustomerContact)
class CustContactAdmin(admin.ModelAdmin):
	list_display = ['contact', 'company']
	list_filter = ['company']

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']
	list_filter = ['name']

@admin.register(Regime)
class RegimeAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']
	list_filter = ['name']

@admin.register(PersonType)
class PersonTypeAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']
	list_filter = ['name']