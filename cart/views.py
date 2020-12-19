from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from catalog.models import Product, Category
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.
@require_POST
def cart_add(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	form = CartAddProductForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(product=product, quantity=float(cd['quantity']), price=float(cd['price']), override_quantity=cd['override'])
		messages.success(request, f'¡El item ha sido agregado a la orden!')
	return redirect('orders:orders_product_list')

@require_POST
def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	messages.success(request, f'¡El item ha sido quitado de la orden!')
	return redirect('orders:orders_product_list')

@login_required
def cart_clear(request):
	cart = Cart(request)
	cart.clear()
	messages.success(request, f'¡Los items de orden han sido eliminados!')
	return redirect('dashboard')
