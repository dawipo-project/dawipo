from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from catalog.models import Product, Category
from customers.models import Customer
from cart.forms import CartAddProductForm
from .tasks import order_created, order_edited
from .forms import OrderCreateForm, OrderEditForm
from .models import OrderItem, Order, OrderChange
from cart.cart import Cart
import datetime
import weasyprint
from io import BytesIO

# Create your views here.
@login_required
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

@login_required
def order_create(request):
	customers = Customer.objects.filter(company=request.user.profile.company)
	categories = Category.objects.filter(company=request.user.profile.company)
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
					tax=item['tax'],
					quantity=item['quantity'])
			cart.clear()
			order_created.delay(order.id, request.user.email)
			return render(request, 'orders/created.html', {'categories': categories, 'order': order})
	else:
		form = OrderCreateForm()
	return render(request, 'orders/create.html', {'cart': cart, 'form': form, 
		'customers': customers, 'categories': categories})

@login_required
def download_order_pdf(request, order_id):
	today = datetime.date.today()
	order = get_object_or_404(Order, id=order_id)
	items = OrderItem.objects.filter(order_id=order_id)
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
	html = render_to_string('orders/pdf.html', {'order': order, 'today': today, 'items': items})
	stylesheets = [
		weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css'), 
		weasyprint.CSS('https://fonts.googleapis.com/css2?family=Lato&display=swap')
	]
	weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=stylesheets)
	return response

@login_required
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

# @login_required
# def db_export_pdf(request):
# 	closest_orders = Order.objects.filter(company=request.user.profile.company).exclude(
#         status='canceled').exclude(status='pre-order').exclude(status='delivered').order_by('due_date')
# 	response = HttpResponse(content_type='application/pdf')
# 	response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
# 	html = render_to_string('orders/pdf.html', {'order': order, 'today': today, 'items': items})
# 	stylesheets = [
# 		weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css'), 
# 		weasyprint.CSS('https://fonts.googleapis.com/css2?family=Lato&display=swap')
# 	]
# 	weasyprint.HTML(string=html).write_pdf(response, stylesheets=stylesheets)
# 	# order_created.delay(order.id, request.user.email)
# 	return response

class OrderList(ListView, LoginRequiredMixin):
	model = Order
	paginate_by = 10
	context_object_name = 'orders'
	template_name = 'orders/order_list.html'

	def get_queryset(self):
		queryset = Order.objects.filter(company=self.request.user.profile.company)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(OrderList, self).get_context_data(**kwargs)
		context['customers'] = Customer.objects.filter(company=self.request.user.profile.company)
		context['categories'] = Category.objects.filter(company=self.request.user.profile.company)
		return context

@login_required
def order_detail(request, order_id):
	customers = Customer.objects.filter(company=request.user.profile.company)
	categories = Category.objects.filter(company=request.user.profile.company)
	order = Order.objects.get(id=order_id)
	items = OrderItem.objects.filter(order_id=order_id)
	return render(request, 'orders/detail.html', {
		'order': order, 
		'items': items, 
		'categories': categories, 
		'customers': customers})

@staff_member_required
def admin_order_detail(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	return render(request, 'admin/orders/detail.html', {'order': order})