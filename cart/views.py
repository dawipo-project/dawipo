from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from catalog.models import Product, Category
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.
@require_POST
def cart_add(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	form = CartAddProductForm(request.POST)
	import pdb; pdb.set_trace()
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(product=product, quantity=cd['quantity'], price=cd['price'], override_quantity=cd['override'])
	return redirect('orders:orders_product_list')

@require_POST
def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	return redirect('orders:orders_product_list')

@login_required
def cart_clear(request):
	cart = Cart(request)
	cart.clear()
	return redirect('dashboard')
