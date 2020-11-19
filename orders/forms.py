from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['customer', 'due_date']
		exclude = ('company',)

class OrderEditForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['due_date', 'status']
		exclude = ('customer', 'company')
