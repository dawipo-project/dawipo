from django.contrib import admin
from django import forms
from django.shortcuts import redirect, render
from .models import Category, Product
import csv
import datetime
from django.http import HttpResponse

# Actions
def export_to_csv(modeladmin, request, queryset):
	opts = modeladmin.model._meta
	content_disposition = f'attachment; filename={opts.verbose_name}.csv'
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

class CsvImportForm(forms.Form):
	csv_file = forms.FileField()

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'sku', 'image', 'description', 
        	'observations', 'price_1', 'price_2', 'price_3',
            'tax', 'available']
	list_filter = ['available', 'created', 'updated']
	list_editable = ['price_1', 'price_2', 'price_3', 'available']
	prepopulated_fields = {'slug': ('name',)}
	actions = [export_to_csv]

	change_list_template = 'orders/csv_link.html'

	def import_csv(self, request):
		if request.method == 'POST':
			csv_file = request.FILES['csv_file']
			reader = csv.reader(csv_file)

			self.message_user(request, 'The file has been imported')
			return redirect('..')
		form = CsvImportForm()
		context = {'form': form}
		return render(request, 'admin/csv_form.html', context)
