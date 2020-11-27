from django.db import models
from company.models import Company

# Create your models here.
class CustomFields(models.Model):
	company = models.ForeignKey(Company, on_delete=models.CASCADE)
	table_name = models.CharField(max_length=50)
	entity_id = models.IntegerField()
	string_1 = models.CharField(max_length=50)
	string_2 = models.CharField(max_length=50)
	string_3 = models.CharField(max_length=50)
	string_4 = models.CharField(max_length=50)
	string_5 = models.CharField(max_length=50)
	string_6 = models.CharField(max_length=50)
	string_7 = models.CharField(max_length=50)
	string_8 = models.CharField(max_length=50)
	string_9 = models.CharField(max_length=50)
	string_10 = models.CharField(max_length=50)