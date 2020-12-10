from celery import task
from django.core.mail import send_mail, EmailMessage
from .models import Order, OrderItem
from django.template.loader import render_to_string
import weasyprint
from django.conf import settings
from io import BytesIO

@task
def order_created(order_id, email, out):
	order = Order.objects.get(id=order_id)
	subject = f'Order No. {order.id}'
	message = f'Dear {order.customer.first_name} {order.customer.last_name},\n\nA pre-order has been placed in our system for {order.customer.name}, which you requested.\nYour order id is {order.id}. You may find the corresponding document attached to this message.'
	email = EmailMessage(subject, message, 'no_reply@dawipo.co', [order.customer.email, email])
	email.attach(f'Orden No. {order.id}.pdf', out.getvalue(), 'application/pdf')
	email.send()

@task
def order_edited(order_id, new_status):
	order = Order.objects.get(id=order_id)
	subject = f'Changes on Order No. {order.id}'
	message = f'Dear {order.customer.first_name} {order.customer.last_name},\n\nYour order No. {order.id} has been updated in our system, and its new status is {new_status}.'
	mail_sent = send_mail(subject, message, 'no_reply@dawipo.co', [order.customer.email])
	return mail_sent