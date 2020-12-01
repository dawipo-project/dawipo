from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import Customer
from catalog.models import Category
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class CustomerRegistrationView(CreateView, LoginRequiredMixin):
	model = Customer
	template_name = 'customers/create.html'
	fields = ['name', 'address', 'city', 'zipcode',
	'first_name', 'last_name', 'email']

	def form_valid(self, form):
		form.instance.company = self.request.user.profile.company
		return super(CustomerRegistrationView, self).form_valid(form)

	def get_success_url(self):
		return reverse_lazy('orders:order_create')

	def get_context_data(self, **kwargs):
		context = super(CustomerRegistrationView, self).get_context_data(**kwargs)
		context['customers'] = Customer.objects.filter(company=self.request.user.profile.company)
		context['categories'] = Category.objects.filter(company=self.request.user.profile.company)
		return context

class CustomerList(ListView, LoginRequiredMixin):
	model = Customer
	paginate_by = 10
	context_object_name = 'orders'
	template_name = 'customers/list.html'

	def get_queryset(self):
		queryset = Customer.objects.filter(company=self.request.user.profile.company)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(CustomerList, self).get_context_data(**kwargs)
		context['customers'] = Customer.objects.filter(company=self.request.user.profile.company)
		context['categories'] = Category.objects.filter(company=self.request.user.profile.company)
		return context