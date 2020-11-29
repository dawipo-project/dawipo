from django.contrib import admin
from .models import Category, Product
import csv
import datetime
from django.http import HttpResponse

# Actions
def export_to_csv(modeladmin, request, queryset):
	opts = modeladmin.model._meta
	content_disposition = 'attachment; filename={opts.verbose_name}.csv'
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = content_disposition
	writer = csv.writer(response)

	fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
	writer.writerow([field.verbose_name for field in fields])

	for obj in queryset:
		data_row = []
		for field in fields:
			value = getattr(obj, field.name)
			if isinstance(value, datetime.datetime):
				value = value.strftime('%d/%m/%Y')
			data_row.append(value)
		writer.writerow(data_row)
	return response

export_to_csv.short_description = 'Export to CSV'

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
	actions = [export_to_csv]