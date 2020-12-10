from celery import task
from django.core.mail import send_mail, EmailMessage
from .models import Order, OrderItem
from django.template.loader import render_to_string
import weasyprint
from django.conf import settings
from io import BytesIO

@task
def order_created(order_id, email, request):
	order = Order.objects.get(id=order_id)
	today = order.created
	items = OrderItem.objects.filter(order_id=order_id)
	logo_url = request.build_absolute_uri()
	logo_url += request.user.profile.company.logo.url
	html = render_to_string('orders/pdf.html', {'order': order, 'today': today, 'items': items, 'logo_url': logo_url}, request=request)
	stylesheets = [
		weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css'), 
		weasyprint.CSS('https://fonts.googleapis.com/css2?family=Lato&display=swap')
	]
	out = BytesIO()
	weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(out, stylesheets=stylesheets)
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