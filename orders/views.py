from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from catalog.models import Product, Category
from customers.models import Customer
from cart.forms import CartAddProductForm
from .tasks import order_created, order_edited
from .forms import OrderCreateForm, OrderEditForm, ItemUpdateForm
from .models import OrderItem, Order, OrderChange, PaymentMethod
from cart.cart import Cart
import datetime
import weasyprint
from io import BytesIO
from django.contrib import messages

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
	payments = PaymentMethod.objects.filter(company=request.user.profile.company)
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
			url = request.build_absolute_uri()
			request_json = request.__dict__
			logo_url = url + request.user.profile.company.logo.url
			order_created.delay(order.id, request.user.email, url, logo_url, request=request_json)
			return render(request, 'orders/created.html', {'categories': categories, 'order': order})
	else:
		form = OrderCreateForm()
	return render(request, 'orders/create.html', {'cart': cart, 'form': form, 
		'customers': customers, 'categories': categories, 'payments': payments})

@login_required
def download_order_pdf(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	today = order.created
	items = OrderItem.objects.filter(order_id=order_id)
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
	logo_url = request.build_absolute_uri()
	logo_url += request.user.profile.company.logo.url
	html = render_to_string('orders/pdf.html', {'order': order, 'today': today, 'items': items, 'logo_url': logo_url}, request=request)
	stylesheets = [
		weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css'), 
		weasyprint.CSS('https://fonts.googleapis.com/css2?family=Lato&display=swap')
	]
	weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=stylesheets)
	return response

@login_required
def order_edit(request, order_id):
	payments = PaymentMethod.objects.filter(company=request.user.profile.company)
	customers = Customer.objects.filter(company=request.user.profile.company)
	categories = Category.objects.filter(company=request.user.profile.company)
	today = datetime.date.today()
	order = get_object_or_404(Order, id=order_id)
	order_items = OrderItem.objects.filter(order_id=order_id)
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
			messages.success(request, f'¡La orden {order.id} ha sido editada exitosamente!')
			return redirect('orders:order_detail', order.id)
	else:
		edit_form = OrderEditForm(instance=order)
	return render(request, 'orders/edit.html', {'form': edit_form, 'categories': categories, 
		'customers': customers, 'order': order, 'items': order_items, 'today': today, 'payments': payments})

class UpdateOrderItem(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = OrderItem
	fields = ['quantity']
	success_message = '¡Los items de la orden han sido actualizados!'

	def get_success_url(self):
		order = Order.objects.get(id=self.object.order.id)
		return reverse_lazy('orders:order_edit', args=[order.id])

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