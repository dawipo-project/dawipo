from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from company.models import Company
from customers.models import Customer
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .forms import ProductEditForm, ProductCreateForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
import csv
from django.http import HttpResponse

# Create your views here.
@login_required
def export_csv(request, queryset):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = f'filename=closest_orders.csv'
	writer = csv.writer(response)
	writer.writerow(['Id de Producto', 'Categoría', 'Nombre del producto', 'SKU', 'Código de barras',
    	'Marca', 'Proveedor', 'Color', 'Medidas', 'Descripción', 'Observaciones', 'Precio 1', 'Precio 2',
    	'Precio 3', 'Impuesto (%)', 'Costo de fabricación'])
	for item in queryset:
		writer.writerow([item.id, item.category.name, item.name, item.sku, item.barcode, item.brand,
        	item.provider, item.color, item.measures, item.description, item.observations, item.price_1,
        	item.price_2, item.price_3, item.tax, item.fabrication_cost])
	return response

@login_required
def product_list(request, category_slug=None):
	customers = Customer.objects.filter(company=request.user.profile.company)
	categories = Category.objects.filter(company=request.user.profile.company)
	products = Product.objects.filter(category__in=categories)
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)
		return render(request, 'catalog/product/list.html', {'category': category,  
			'products': products, 'categories': categories, 'customers': customers})
	return render(request, 'catalog/product/list.html', {'products': products, 'categories': categories, 'customers': customers})

@login_required
def product_detail(request, id, slug):
	customers = Customer.objects.filter(company=request.user.profile.company)
	categories = Category.objects.filter(company=request.user.profile.company)
	product = get_object_or_404(Product, id=id, slug=slug)
	return render(request, 'catalog/product/detail.html', {'product': product, 'categories': categories, 'customers': customers})

@login_required
def edit(request, id, slug):
	customers = Customer.objects.filter(company=request.user.profile.company)
	categories = Category.objects.filter(company=request.user.profile.company)
	products = Product.objects.filter(category__in=categories)
	product = get_object_or_404(Product, id=id, slug=slug)
	if request.method == 'POST':
		product_form = ProductEditForm(instance=product, data=request.POST, files=request.FILES)
		if product_form.is_valid():
			product_form.save()
			messages.success(request, f'¡El producto {product.name} ha sido editado exitosamente!')
			return render(request, 'catalog/product/list.html', {'categories': categories, 'customers': customers, 'products': products})
		product_form = ProductEditForm()
		return render(request, 'catalog/product/edit.html', {'product_form': product_form, 'product': product,
			'categories': categories, 'customers': customers})
	else:
		product_form = ProductEditForm(instance=product)
	return render(request, 'catalog/product/edit.html', {'product_form': product_form, 'product': product,
		'categories': categories, 'customers': customers})

class CategoryCreate(SuccessMessageMixin, CreateView, LoginRequiredMixin):
	model = Category
	fields = ['name']
	template_name = 'catalog/category/add_category.html'
	success_message = '¡La categoría ha sido registrada exitosamente!'

	def form_valid(self, form):
		form.instance.company = self.request.user.profile.company
		return super(CategoryCreate, self).form_valid(form)
	
	def get_success_url(self):
		return reverse_lazy('catalog:product_list')

	def get_context_data(self, **kwargs):
		context = super(CategoryCreate, self).get_context_data(**kwargs)
		context['customers'] = Customer.objects.filter(company=self.request.user.profile.company)
		context['categories'] = Category.objects.filter(company=self.request.user.profile.company)
		return context

@login_required
def create_product(request):
	customers = Customer.objects.filter(company=request.user.profile.company)
	categories = Category.objects.filter(company=request.user.profile.company)
	products = Product.objects.filter(category__in=categories)
	if request.method == 'POST':
		category_name = request.POST['category']
		category = Category.objects.get(id=category_name)
		form = ProductCreateForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			cd = form.cleaned_data
			product = form.save(commit=False)
			product.category = category
			product.save()
			messages.success(request, f'¡El producto {product.name} ha sido registrado exitosamente!')
			return render(request, 'catalog/product/list.html', {
				'categories': categories,
				'customers': customers,
				'products': products
				})
	else:
		form = ProductCreateForm()
	return render(request, 'catalog/product/add_product.html', {'product_form': form,
		'categories': categories, 'customers': customers})

class ProductList(ListView, LoginRequiredMixin):
	paginate_by = 10
	model = Product
	context_object_name = 'products'
	template_name = 'catalog/product/product_list.html'

	def get_queryset(self):
		categories = Category.objects.filter(company=self.request.user.profile.company)
		queryset = Product.objects.filter(category__in=categories)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(ProductList, self).get_context_data(**kwargs)
		context['customers'] = Customer.objects.filter(company=self.request.user.profile.company)
		context['categories'] = Category.objects.filter(company=self.request.user.profile.company)
		return context

class CategoryProductList(ListView, LoginRequiredMixin):
	paginate_by = 10
	template_name = 'catalog/product/product_list.html'
	context_object_name = 'products'
	
	def get_queryset(self):
		self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
		queryset = Product.objects.filter(category=self.category)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(CategoryProductList, self).get_context_data(**kwargs)
		context['customers'] = Customer.objects.filter(company=self.request.user.profile.company)
		context['categories'] = Category.objects.filter(company=self.request.user.profile.company)
		context['category'] = self.category
		context['category_slug'] = self.category.slug
		return context