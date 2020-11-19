from django.db import models
from catalog.models import Product
from customers.models import Customer
from company.models import Company
from django.contrib.auth.models import User

# Create your models here.
STATUS_CHOICES = (
	('pre-order', 'Pre-order'),
	('confirmed', 'Confirmed'),
	('awaiting-advance-payment', 'Awaiting advance payment'),
	('in-production', 'En Producción'),
	('scheduled', 'Scheduled for dispatch'),
	('dispatched', 'Dispatched'),
	('delivered', 'Delivered'),
	('canceled', 'Canceled'),
)

class Order(models.Model):
	company = models.ForeignKey(Company, related_name='company_orders', on_delete=models.CASCADE)
	user = models.ForeignKey(User, related_name='order_author', on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, related_name='order_customer', on_delete=models.CASCADE)
	due_date = models.DateField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=25,
		choices=STATUS_CHOICES,
		default='pre-order'
	)

	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return f'Order No. {self.id}'

	def get_total_cost(self):
		return sum(item.get_cost() for item in self.items.all())

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
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return str(self.id)

	def get_cost(self):
		return self.price * self.quantity
