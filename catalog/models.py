from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from company.models import Company

# Create your models here.
class Category(models.Model):
	company = models.ForeignKey(Company, related_name='company_categories', on_delete=models.CASCADE)
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, unique=True)

	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('catalog:product_list_by_category', args=[self.slug])

	def save(self):
		self.slug = slugify(self.name)
		super(Category, self).save()

class Product(models.Model):
	category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, db_index=True)
	sku = models.CharField(max_length=20, db_index=True, blank=True, null=True)
	image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
	description = models.TextField(blank=True)
	observations = models.TextField(blank=True)
	color = models.CharField(max_length=15, blank=True) # Observaciones
	measures = models.TextField(blank=True) # Observaciones
	retail_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Separador de miles
	whole_sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) # Separador de miles
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def get_absolute_url(self):
		return reverse('catalog:product_detail', args=[self.id, self.slug])

	class Meta:
		ordering = ('name',)
		index_together = (('id', 'slug'),)

	def save(self):
		self.slug = slugify(self.name)
		super(Product, self).save(commit=False)
		if self.sku:
			self.sku = str(self.category.id) + str(self.id)
		super(Product, self).save()

	def __str__(self):
		return self.name