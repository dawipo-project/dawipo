from django.db import models
from company.models import Company

# Create your models here.
class DocumentType(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return f'{self.name}'

class Regime(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return f'Régimen {self.name}'

class PersonType(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return f'Persona {self.name}'

class CustomerContact(models.Model):
	contact = models.CharField(max_length=50)
	company = models.ForeignKey(Company, related_name='company_customer_contacts', on_delete=models.CASCADE)

	class Meta:
		ordering = ('contact',)

	def __str__(self):
		return f'{self.contact}'

class Customer(models.Model):
	company = models.ForeignKey(Company, related_name='company_customers', on_delete=models.CASCADE)
	name = models.CharField(max_length=70)
	document_type = models.ForeignKey(DocumentType, related_name='customer_document_type', 
		on_delete=models.CASCADE, null=True, blank=True)
	document = models.CharField(max_length=30, null=True, blank=True)
	regime = models.ForeignKey(Regime, related_name='customer_regime', 
		on_delete=models.CASCADE, null=True, blank=True)
	person_type = models.ForeignKey(PersonType, related_name='customer_person',
		null=True, blank=True, on_delete=models.CASCADE)
	address = models.CharField(max_length=200)
	city =  models.CharField(max_length=30)
	zone = models.CharField(max_length=50, null=True, blank=True)
	phone_number = models.CharField(max_length=30, null=True, blank=True)
	zipcode = models.CharField(max_length=10, null=True, blank=True)
	first_name = models.CharField(max_length=20, null=True, blank=True)
	last_name = models.CharField(max_length=20, null=True, blank=True)
	email = models.EmailField()
	active = models.BooleanField(default=True)
	cust_contact = models.ForeignKey(CustomerContact, on_delete=models.CASCADE, blank=True, null=True)

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return f'Customer {self.name}'