from decimal import Decimal
from django.conf import settings
from catalog.models import Product

class Cart(object):
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart

	def add(self, product, price, quantity=1, override_quantity=False):
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {'quantity': 0, 'price': str(price), 'tax': str(product.tax)}
		if override_quantity:
			self.cart[product_id]['quantity'] = quantity
		else:
			self.cart[product_id]['quantity'] += quantity
		self.save()

	def save(self):
		self.session.modified = True

	def remove(self, product):
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product.id]
			self.save()

	def __iter__(self):
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)
		cart = self.cart.copy()
		for product in products:
			cart[str(product.id)]['product'] = product
		for item in cart.values():
			item['price'] = item['price']
			item['total_tax'] = item['tax'] * item['quantity']
			item['total_price'] = item['price'] * item['quantity']
			yield item

	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):
		return sum(item['price'] * item['quantity'] for item in self.cart.values())

	def get_total_tax(self):
		return sum(item['tax'] * item['quantity'] for item in self.cart.values())

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.save()
