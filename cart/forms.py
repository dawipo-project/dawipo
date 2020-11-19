from django import forms

class CartAddProductForm(forms.Form):
	quantity = forms.IntegerField(
		label ='Amount'
	)
	override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


	