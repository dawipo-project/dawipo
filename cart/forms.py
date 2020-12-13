from django import forms

class CartAddProductForm(forms.Form):
	price = forms.DecimalField(decimal_places=2, localize=True, required=False)
	quantity = forms.IntegerField(
		label ='Amount'
	)
	override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


	