from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from catalog.models import Product, Category
from customers.models import Customer
from cart.forms import CartAddProductForm
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from .models import OrderItem, Order, OrderChange
from .forms import OrderCreateForm, OrderEditForm
from .tasks import order_created, order_edited
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import datetime

# Create your views here.
def product_list(request, category_slug=None):
	categories = Category.objects.filter(company=request.user.profile.company)
	# Esta vista filtra los productos para que no se pueda
	# agregar productos no disponibles a las ordenes
	products = Product.objects.filter(available=True, category__in=categories)
	cart_form = CartAddProductForm()
	if category_slug:
		# Filtro por categorías
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)
	return render(request, 'orders/list.html', {'categories': categories,  
		'products': products,
		'cart_product_form': cart_form})

def order_create(request):
	customers = Customer.objects.filter(company=request.user.profile.company)
	categories = Category.objects.filter(company=request.user.profile.company)
	today = datetime.date.today()
	cart = Cart(request)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			order = form.save(commit=False)
			order.user = request.user
			order.company = request.user.profile.company
			order.save()
			for item in cart:
				OrderItem.objects.create(order=order,
					product=item['product'],
					price=item['price'],
					quantity=item['quantity'])
			cart.clear()
			order_created.delay(order.id, request.user.email)
			return render(request, 'orders/created.html', {'order': order})
	else:
		form = OrderCreateForm()
	return render(request, 'orders/create.html', {'cart': cart, 'form': form, 
		'customers': customers, 'categories': categories, 'today': today})

def order_edit(request, order_id):
	customers = Customer.objects.filter(company=request.user.profile.company)
	categories = Category.objects.filter(company=request.user.profile.company)
	today = datetime.date.today()
	order = get_object_or_404(Order, id=order_id)
	order_items = OrderItem.objects.filter(order_id=order.id)
	status = order.status
	if request.method == 'POST':
		edit_form = OrderEditForm(instance=order, data=request.POST)
		if edit_form.is_valid():
			cd = edit_form.cleaned_data
			new_status = cd['status']
			if status != new_status:
				change = f'From status {status} to {new_status}'
				OrderChange.objects.create(
					order=order,
					change=change,
					initial_status=status,
					final_status=new_status
				)
				order_edited.delay(order.id, new_status)
			edit_form.save()
			return redirect('orders:order_detail', order.id)
	else:
		edit_form = OrderEditForm(instance=order)
	return render(request, 'orders/edit.html', {'form': edit_form, 'categories': categories, 
		'customers': customers, 'order': order, 'items': order_items, 'today': today})


class OrderList(ListView):
	model = Order
	paginate_by = 7
	context_object_name = 'orders'
	template_name = 'orders/order_list.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)

	def get_queryset(self):
		queryset = Order.objects.filter(company=self.request.user.profile.company)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(OrderList, self).get_context_data(**kwargs)
		context['customers'] = Customer.objects.filter(company=self.request.user.profile.company)
		context['categories'] = Category.objects.filter(company=self.request.user.profile.company)
		return context

def order_detail(request, order_id):
	customers = Customer.objects.filter(company=request.user.profile.company)
	categories = Category.objects.filter(company=request.user.profile.company)
	order = Order.objects.get(id=order_id)
	items = OrderItem.objects.filter(order_id=order_id)
	return render(request, 'orders/detail.html', {'order': order, 'items': items, 'categories': categories, 'customers': customers})
