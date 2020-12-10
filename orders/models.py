from django.db import models
from catalog.models import Product
from customers.models import Customer
from company.models import Company
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class OrderStatus(models.Model):
	name = models.CharField(max_length=50, db_index=True)
	es_name = models.CharField(max_length=50, null=True, blank=True)
	slug = models.SlugField(max_length=50, db_index=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'order status'
		verbose_name_plural = 'order statuses'

	def __str__(self):
		return f'Order status {self.name}'

	def save(self):
		self.slug = slugify(self.name)
		super(OrderStatus, self).save()

class PaymentMethod(models.Model):
	company = models.ForeignKey(Company, related_name='payment_company', 
		on_delete=models.CASCADE, blank=True, null=True)
	name = models.CharField(max_length=100, db_index=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'payment method'
		verbose_name_plural = 'payment methods'

	def __str__(self):
		return f'Payment by {self.name}'

class Order(models.Model):
	STATUS_CHOICES = (
		('pre-order', 'Pre-orden'),
		('confirmed', 'Confirmada'),
		('awaiting-advance-payment', 'Esperando anticipo'),
		('in-production', 'En Producción'),
		('scheduled', 'Programada para despacho'),
		('dispatched', 'Despachada'),
		('delivered', 'Entregada'),
		('canceled', 'Cancelada'),
	)
	INCOTERM_CHOICES = (
		('EXW', 'EXW'),
		('FCA', 'FCA'),
		('CPT', 'CPT'),
		('CIP', 'CIP'),
		('DAP', 'DAP'),
		('DPU', 'DPU'),
		('DDP', 'DDP'),
		('FAS', 'FAS'),
		('FOB', 'FOB'),
		('CFR', 'CFR'),
		('CIF', 'CIF'),
	)
	TRANSPORT_CHOICES = (
		('air', 'Aéreo'),
		('road', 'Terrestre'),
		('ocean', 'Marítimo'),
		('package', 'Paquetería'),
	)
	company = models.ForeignKey(Company, related_name='company_orders', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='order_author', on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, related_name='order_customer', on_delete=models.CASCADE)
	due_date = models.DateField()
	incoterm = models.CharField(max_length=3, choices=INCOTERM_CHOICES, blank=True, null=True)
	delivery_site = models.CharField(max_length=50, null=True, blank=True)
	transport = models.CharField(max_length=9, choices=TRANSPORT_CHOICES, blank=True, null=True)
	country_of_origin = models.CharField(max_length=20, null=True, blank=True)
	tax = models.BooleanField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='pre-order')
	shipping = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
	payment_method = models.ForeignKey(PaymentMethod, 
		related_name='order_payment', on_delete=models.CASCADE, null=True, blank=True)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return f'Order No. {self.id}'

	def get_cost(self):
		return round((sum(item.get_cost() for item in self.items.all())) - (sum(item.get_tax() for item in self.items.all())), 2)

	def get_total_tax(self):
		if self.tax:
			return round(sum((item.get_cost() / 100) * item.tax for item in self.items.all()), 2)
		else:
			return 0

	def get_total_cost(self):
		return round((self.get_cost() + self.get_total_tax() + self.shipping),2)

class OrderChange(models.Model):
	order = models.ForeignKey(Order, related_name='order_order_changes', on_delete=models.CASCADE)
	change = models.CharField(max_length=100)
	initial_status = models.CharField(max_length=25)
	final_status = models.CharField(max_length=25)
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('-date',)

	def __str__(self):
		return f'Order change to order {self.order.id}.\nInitial status: {self.initial_status}\nFinal status: {self.final_status}'

class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=20, decimal_places=2)
	tax = models.DecimalField(max_digits=5, decimal_places=2, null=True, default=0)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return str(self.id)

	def get_cost(self):
		if self.order.tax:
			return round((self.price - ((self.price / 100) * self.tax)) * self.quantity, 2)
		else:
			return round(self.price * self.quantity, 2)


	def get_tax(self):
		return round((self.price * (self.tax / 100)) * self.quantity, 2)
