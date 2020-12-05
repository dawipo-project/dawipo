# Python
import datetime
# NumPy
import numpy as np
#WeasyPrint
import weasyprint
# Django
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
# Apps de Dawipo
from .forms import LoginForm, UserEditForm, ProfileEditForm
from .models import Profile
from catalog.models import Category, Product
from orders.models import Order, OrderChange
from customers.models import Customer

# Create your views here.
def user_login(request):
    '''
    Esta vista implementa la funcionalidad de login de usuarios en DAWIPO. 
    Los usuarios pueden iniciar sesión utilizando su nombre de usuario o 
    su correo electrónico, y su contraseña.
    '''
    # Si al petición es por el método GET, el formulario aparece vacío
    if request.method == 'POST':
        # Cargamos los datos que se envíen desde el formulario por método POST
        form = LoginForm(request.POST)
        if form.is_valid():
            # Si los datos son válidos, se procede a autenticar contra la base de datos
            cd = form.cleaned_data
            user = authenticate(
                request,
                username = cd['username'],
                password = cd['password']
            )
            if user is not None:
                # Si la cuenta no está activa, no inicia sesión
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully.')
                else:
                    return HttpResponse('Your account has not been activated.')
            else:
                # Si los datos son incorrectos, no inicia sesión
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def dashboard(request):
    # Contexto
    customers = Customer.objects.filter(company=request.user.profile.company)
    categories = Category.objects.filter(company=request.user.profile.company)
    today = datetime.date.today()
    year_ago = today - datetime.timedelta(days=365)
    order_changes_one = OrderChange.objects.order_by(
        'order_id').filter(
        final_status='confirmed').filter(
        date__gte=year_ago).filter(
        order__company=request.user.profile.company)
    total_value = 0
    # Primer gráfico
    total_order_changes = OrderChange.objects.none()
    current_day = today
    for i in range(365):
        previous_day = current_day - datetime.timedelta(days=1)
        order_changes = OrderChange.objects.order_by(
            'order_id').filter(
            final_status='confirmed').filter(
            date__gte=previous_day).distinct('order_id').filter(
            order__company=request.user.profile.company)
        total_order_changes = total_order_changes | order_changes
        current_day = previous_day
    for item in total_order_changes:
        try:
            order = Order.objects.get(id=item.order_id, company=request.user.profile.company)
            total_value += order.get_total_cost()
        except Order.DoesNotExist:
            pass
    past_year_value = 0
    total_order_changes = OrderChange.objects.none()
    for i in range(365):
        previous_day = current_day - datetime.timedelta(days=1)
        order_changes = OrderChange.objects.order_by(
            'order_id').filter(
            final_status='confirmed').filter(
            date__gte=previous_day).exclude(
            date__gte=current_day).distinct('order_id').filter(
            order__company=request.user.profile.company)
        total_order_changes = total_order_changes | order_changes
        current_day = previous_day
    for item in total_order_changes:
        try:
            order = Order.objects.get(id=item.order_id, company=request.user.profile.company)
            past_year_value += order.get_total_cost()
        except Order.DoesNotExist:
            pass
    months_list = get_months(today.month)
    year_orders = OrderChange.objects.order_by(
        'order_id').filter(
        date__gte=year_ago).filter(
        final_status='confirmed').distinct(
        'order_id').filter(
        order__company=request.user.profile.company)
    year_orders_per_month = get_orders_per_month(year_orders, months_list)
    two_years_ago = year_ago - datetime.timedelta(days=365)
    last_year_orders = OrderChange.objects.order_by(
        'order_id').filter(
        final_status='confirmed').exclude(
        date__gte=year_ago).filter(
        date__gte=two_years_ago).distinct(
        'order_id').filter(
        order__company=request.user.profile.company)
    last_year_orders_per_month = get_orders_per_month(last_year_orders, months_list)
    year_orders = list(year_orders_per_month.values())
    last_year_orders = list(last_year_orders_per_month.values())

    # Segundo gráfico
    customers = Customer.objects.filter(company=request.user.profile.company)[:10]
    status_orders = dict()
    for status_tuple in Order.STATUS_CHOICES:
        status_orders[status_tuple[0]] = list()
    for k in status_orders.keys():
        value = list()
        for customer in customers:
            filtered_query = Order.objects.filter(
                customer=customer).filter(
                status=k).count()
            value.append(filtered_query)
        status_orders[k] = value
    for status_tuple in Order.STATUS_CHOICES:
        status_orders[status_tuple[1]] = status_orders.pop(status_tuple[0])
    customers_list = list()
    customers = Customer.objects.filter(company=request.user.profile.company)[:10]
    for customer in customers:
        name = customer.name
        if len(name) > 20:
            name = name[:15]
            name += '...'
        if ' ' in name:
            name = name.split()
        elif len(name) > 10 and ' ' not in name:
            name = name[:7]
            name += '...'
        customers_list.append(name)
    total_orders = list()
    aux_list = list(status_orders.values())
    for i in range(len(aux_list[0])):
        total = 0
        for item in aux_list:
            total += item[i]
        total_orders.append(total)
    sorted_indexes = list(np.argsort(total_orders))
    sorted_indexes.reverse()
    values_list = list(status_orders.values())
    new_list = list()
    for values in values_list:
        aux_list = list()
        for value in values:
            aux_list.append(value)
        for j in range(len(sorted_indexes)):
            aux_list[j] = values[sorted_indexes[j]]
        new_list.append(aux_list)
    new_cust_list = list()
    for c in range(len(customers_list)):
        new_cust_list.append(customers_list[sorted_indexes[c]])
    status_list = [status_tuple[1] for status_tuple in Order.STATUS_CHOICES]
    status_orders = dict(zip(status_list, new_list))

    # Gráfica de productos más vendidos
    orders = Order.objects.filter(company=request.user.profile.company).exclude(status='pre-order').exclude(status='canceled')
    orders_items = Order.objects.none()
    for order in orders:
        orders_items = orders_items | order.items.all()
    products_dict = dict()
    for item in orders_items:
        name = item.product.name
        products_dict[name] = 0
    for item in orders_items:
        quantity = item.quantity
        products_dict[item.product.name] += quantity
    products_dict = {k: v for k, v in sorted(products_dict.items(), key=lambda item: item[1])}
    products_dict_keys = list(products_dict.keys())
    products_dict_keys.reverse()
    products_dict_keys = products_dict_keys[:5]
    products_dict_values = list(products_dict.values())
    products_dict_values.reverse()
    products_dict_values = products_dict_values[:5]
    products_dict = dict()
    for item in orders_items:
        name = item.product.name
        products_dict[name] = 0
    for item in orders_items:
        quantity = item.quantity
        products_dict[item.product.name] += quantity
    products_dict = {k: v for k, v in sorted(products_dict.items(), key=lambda item: item[1])}
    reordered_keys = list(products_dict.keys())
    reordered_keys.reverse()
    reordered_keys = reordered_keys[:5]
    reordered_values = list(products_dict.values())
    reordered_values.reverse()
    reordered_values = reordered_values[:5]
    for i in range(len(reordered_keys)):
        product = Product.objects.get(name=reordered_keys[i])
        reordered_values[i] = reordered_values[i] * product.price_1
    products_dict = {reordered_keys[i]: reordered_values[i] for i in range(len(reordered_keys))}
    # Tabla de órdenes más cercanas
    closest_orders = Order.objects.filter(company=request.user.profile.company).exclude(
        status='canceled').exclude(status='pre-order').exclude(status='delivered').order_by('due_date')[:10]
    # Ordenes por estado
    status_orders_two = dict()
    for status_tuple in Order.STATUS_CHOICES:
        status_orders_two[status_tuple[0]] = 0
    for k in status_orders_two.keys():
        status_orders_two[k] += Order.objects.filter(status=k).filter(company=request.user.profile.company).count()
    for status_tuple in Order.STATUS_CHOICES:
        status_orders_two[status_tuple[1]] = status_orders_two.pop(status_tuple[0])
    status_orders_labels = list(status_orders_two.keys())
    status_orders_values = list(status_orders_two.values())
    # Indicadores
    confirmed_units = 0
    dispatched_units = 0
    today = datetime.date.today()
    month_ago = today - datetime.timedelta(days=30)
    confirmed_orders = Order.objects.exclude(status='canceled').exclude(status='pre-order').filter(
        created__gte=month_ago).filter(company=request.user.profile.company)
    orders_items = Order.objects.none()
    for order in confirmed_orders:
        orders_items = orders_items | order.items.all()
    for item in orders_items:
        quantity = item.quantity
        confirmed_units += quantity
    dispatched_orders = confirmed_orders.filter(status='dispatched')
    dispatched_orders = dispatched_orders | confirmed_orders.filter(status='delivered')
    orders_items = Order.objects.none()
    for order in dispatched_orders:
        orders_items = orders_items | order.items.all()
    for item in orders_items:
        quantity = item.quantity
        dispatched_units += quantity

    return render(request, 'account/dashboard.html', {'section': dashboard, 
        'customers': customers, 
        'categories': categories,
        'total_value': total_value,
        'past_year_value': past_year_value,
        'last_year_orders': last_year_orders,
        'year_orders': year_orders,
        'months_list': months_list,
        'closest_orders': closest_orders,
        'status_orders': status_orders,
        'customers_list': new_cust_list,
        'products_dict_keys': products_dict_keys,
        'products_dict_values': products_dict_values,
        'products_dict': products_dict,
        'status_orders_labels': status_orders_labels,
        'status_orders_values': status_orders_values,
        'confirmed_units': confirmed_units,
        'dispatched_units': dispatched_units
        })

@login_required
def db_export_pdf(request):
    today = datetime.date.today()
    closest_orders = Order.objects.filter(company=request.user.profile.company).exclude(
        status='canceled').exclude(status='pre-order').exclude(status='delivered').order_by('due_date')[:20]
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=closest_orders.pdf'
    html = render_to_string('account/pdf.html', {'orders': closest_orders, 'today': today, 'request': request})
    stylesheets = [
        weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css'), 
        weasyprint.CSS('https://fonts.googleapis.com/css2?family=Lato&display=swap')
    ]
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, stylesheets=stylesheets)
    return response

def create_cust_dict(customers):
    customer_dict = {}
    orders_per_cust = {}
    for choice in Order.status.field.choices:
        orders_per_cust[choice[0]] = 0
    for customer in customers:
        customer_dict[customer.name] = orders_per_cust
    return customer_dict

def get_orders_per_month(order_changes, month_list):
    changes_list = [0 for month in month_list]
    for i in range(len(month_list)):
        for item in order_changes:
            if item.date.strftime('%b') == month_list[i]:
                changes_list[i] += 1
    orders_dict = dict(zip(month_list, changes_list))
    return orders_dict

def get_months(month):
    actual_month = month
    months_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    months_list = (months_list[-actual_month:] + months_list[:-actual_month])
    return months_list

@login_required
def edit(request):
    customers = Customer.objects.filter(company=request.user.profile.company)
    categories = Category.objects.filter(company=request.user.profile.company)
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
        data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 
        'profile_form': profile_form, 
        'categories': categories, 
        'customers': customers})
