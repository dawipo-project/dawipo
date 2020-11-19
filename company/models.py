from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=256)
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=40)
    active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='company/logos', blank=True)

    class Meta:
    	ordering = ('name',)
    	verbose_name = 'company'
    	verbose_name_plural = 'companies'

    def __str__(self):
        return f'Compañía: {self.name}'