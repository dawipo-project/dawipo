from django.contrib import admin
from .models import Contact

# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = ['first_name', 'last_name', 'email', 
	'phone_number', 'organization', 'position']
	list_filter = ['first_name', 'last_name', 'organization', 'position']
