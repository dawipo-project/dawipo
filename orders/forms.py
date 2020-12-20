from django import forms
from .models import Order
from company.models import Company

class OrderCreateForm(forms.ModelForm):
	due_date = forms.DateField(localize=True)
	shipping = forms.DecimalField(decimal_places=2, localize=True, required=False)
	discount = forms.DecimalField(decimal_places=2, required=False, localize=True)

	class Meta:
		model = Order
		fields = ['payment_method', 'customer', 'due_date', 'incoterm', 
		'delivery_site', 'transport', 'country_of_origin', 
		'tax', 'shipping', 'observations', 'discount']
		exclude = ('company',)

class OrderEditForm(forms.ModelForm):
	due_date = forms.DateField(localize=True)
	
	class Meta:
		model = Order
		fields = ['payment_method', 'due_date', 'status', 'incoterm', 
		'delivery_site', 'transport', 'country_of_origin', 'observations']
		exclude = ('customer', 'company')

class ItemUpdateForm(forms.Form):
	price = forms.DecimalField(decimal_places=2, localize=True)
	quantity = forms.IntegerField(
		label ='Amount'
	)
