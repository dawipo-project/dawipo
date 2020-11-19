from django.db import models
from company.models import Company

# Create your models here.
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

	class Meta:
		ordering = ('name',)

	def __str__(self):
		return f'Customer {self.name}'