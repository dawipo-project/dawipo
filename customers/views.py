from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Customer
from catalog.models import Category

# Create your views here.
class CustomerRegistrationView(CreateView):
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
