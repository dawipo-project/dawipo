from django.db import models

# Create your models here.
class Contact(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=40)
	email = models.EmailField()
	phone_number = models.CharField(max_length=20)
	organization = models.CharField(max_length=40)
	position = models.CharField(max_length=40)
	acceptance = models.BooleanField(default=True)