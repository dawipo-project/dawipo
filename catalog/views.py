from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from company.models import Company
from customers.models import Customer
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .forms import ProductEditForm, ProductCreateForm
from django.urls import reverse_lazy

# Create your views here.
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

def product_detail(request, id, slug):
	customers = Customer.objects.filter(company=request.user.profile.company)
	categories = Category.objects.filter(company=request.user.profile.company)
	product = get_object_or_404(Product, id=id, slug=slug)
	return render(request, 'catalog/product/detail.html', {'product': product, 'categories': categories, 'customers': customers})

def edit(request, id, slug):
	customers = Customer.objects.filter(company=request.user.profile.company)
	categories = Category.objects.filter(company=request.user.profile.company)
	product = get_object_or_404(Product, id=id, slug=slug)
	if request.method == 'POST':
		product_form = ProductEditForm(instance=product, data=request.POST, files=request.FILES)
		if product_form.is_valid():
			product_form.save()
	else:
		product_form = ProductEditForm(instance=product)
	return render(request, 'catalog/product/edit.html', {'product_form': product_form, 'product': product,
		'categories': categories, 'customers': customers})

class ProductCreate(CreateView):
	model = Product
	fields = '__all__'
	template_name = 'catalog/product/add_product.html'

	def form_valid(self, form):
		form.instance.category = get_object_or_404(Category, form.instance.category)
		return super(ProductCreate, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('catalog:product_list')

	def get_context_data(self, **kwargs):
		context = super(ProductCreate, self).get_context_data(**kwargs)
		context['customers'] = Customer.objects.filter(company=self.request.user.profile.company)
		context['categories'] = Category.objects.filter(company=self.request.user.profile.company)
		return context

class CategoryCreate(CreateView):
	model = Category
	fields = ['name']
	template_name = 'catalog/category/add_category.html'

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

def create_product(request):
	customers = Customer.objects.filter(company=request.user.profile.company)
	categories = Category.objects.filter(company=request.user.profile.company)
	if request.method == 'POST':
		category_name = request.POST['category']
		category = get_object_or_404(Category, name=category_name)
		form = ProductCreateForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			cd = form.cleaned_data
			product = form.save(commit=False)
			product.category = category
			product.save()
	else:
		form = ProductCreateForm()
	return render(request, 'catalog/product/add_product.html', {'product_form': form,
		'categories': categories, 'customers': customers})

class ProductList(ListView):
	model = Product
	context_object_name = 'products'
	template_name = 'catalog/product/product_list.html'

	def get_context_data(self, **kwargs):
		context = super(ProductList, self).get_context_data(**kwargs)
		context['customers'] = Customer.objects.filter(company=self.request.user.profile.company)
		context['categories'] = Category.objects.filter(company=self.request.user.profile.company)
		return context

class CategoryProductList(ListView):
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