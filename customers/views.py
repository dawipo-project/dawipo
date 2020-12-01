from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import Customer, DocumentType, Regime, PersonType, CustomerContact
from catalog.models import Category
import csv
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
		context['document_types'] = DocumentType.objects.all()
		context['regimes'] = Regime.objects.all()
		context['person_types'] = PersonType.objects.all()
		context['contacts'] = CustomerContact.objects.filter(company=self.request.user.profile.company)
		context['customers'] = Customer.objects.filter(company=self.request.user.profile.company)
		context['categories'] = Category.objects.filter(company=self.request.user.profile.company)
		return context

class CustomerList(ListView, LoginRequiredMixin):
	model = Customer
	paginate_by = 10
	context_object_name = 'customers'
	template_name = 'customers/list.html'

	def get_queryset(self):
		queryset = Customer.objects.filter(company=self.request.user.profile.company)
		return queryset

	def get_context_data(self, **kwargs):
		context = super(CustomerList, self).get_context_data(**kwargs)
		context['customers'] = Customer.objects.filter(company=self.request.user.profile.company)
		context['categories'] = Category.objects.filter(company=self.request.user.profile.company)
		return context

def import_csv(request):
	categories = Category.objects.filter(company=request.user.profile.company)
	file = request.FILES
	reader = csv.reader(file)
	next(reader, None)
	for row in reader:
		try:
			_, created = Customer.objects.get_or_create(
				company=request.user.profile.company,
				name=row[0],
				document_type=row[1],
				document=row[2],
				regime=row[3],
				person_type=row[4],
				address=row[5],
				city=row[6],
				zone=row[7],
				zipcode=row[8],
				phone_number=row[9],
				cellphone=row[10],
				first_name=row[11],
				last_name=row[12],
				email=row[13],
				internal_code=row[14],
				active=True,
				cust_contact=row[15]
			)
		except:
			pass
	return render(request, 'customers/imported.html', {'categories': categories})