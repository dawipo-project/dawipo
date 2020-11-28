from django.db import models
from company.models import Company

# Create your models here.
class CustomerContact(models.Model):
	contact = models.CharField(max_length=50)
	company = models.ForeignKey(Company, related_name='company_customers', on_delete=models.CASCADE)

	class Meta:
		ordering = ('contact',)

	def __str__(self):
		return f'Contacted by {self.contact}'

class Customer(models.Model):
	company = models.ForeignKey(Company, related_name='company_customers', on_delete=models.CASCADE)
	name = models.CharField(max_length=70)
	address = models.CharField(max_length=200)
	city =  models.CharField(max_length=30)
	zipcode = models.CharField(max_length=10)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	email = models.EmailField()
	active = models.BooleanField(default=True)
	cust_contact = models.ForeignKey(CustomerContact, on_delete=models.CASCADE, blank=True, null=True)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return f'Customer {self.name}'