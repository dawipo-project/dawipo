from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def order_created(order_id, email):
	order = Order.objects.get(id=order_id)
	subject = f'Order No. {order.id}'
	message = f'Dear {order.customer.first_name} {order.customer.last_name},\n\nA pre-order has been placed in our system for {order.customer.name}, which you requested.\nYour order id is {order.id}'
	mail_sent = send_mail(subject, message, 'dawipoproject@gmail.com', [order.customer.email, email])
	return mail_sent

@task
def order_edited(order_id, new_status):
	order = Order.objects.get(id=order_id)
	subject = f'Changes on Order No. {order.id}'
	message = f'Dear {order.customer.first_name} {order.customer.last_name},\n\nYour order No. {order.id} has been updated in our system, and its new status is {new_status}.'
	mail_sent = send_mail(subject, message, 'dawipoproject@gmail.com', [order.customer.email])
	return mail_sent