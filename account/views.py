# Python
import datetime
# Django
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Apps de Dawipo
from .forms import LoginForm, UserEditForm, ProfileEditForm
from .models import Profile
from catalog.models import Category
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
        date__gte=year_ago)
    total_value = 0
    # Primer gráfico
    total_order_changes = OrderChange.objects.none()
    current_day = today
    for i in range(365):
        previous_day = current_day - datetime.timedelta(days=1)
        order_changes = OrderChange.objects.order_by(
            'order_id').filter(
            final_status='confirmed').filter(
            date__gte=previous_day).distinct('order_id')
        total_order_changes = total_order_changes | order_changes
        current_day = previous_day
    for item in total_order_changes:
        order = Order.objects.get(id=item.order_id)
        total_value += order.get_total_cost()
    past_year_value = 0
    total_order_changes = OrderChange.objects.none()
    for i in range(365):
        previous_day = current_day - datetime.timedelta(days=1)
        order_changes = OrderChange.objects.order_by(
            'order_id').filter(
            final_status='confirmed').filter(
            date__gte=previous_day).exclude(
            date__gte=current_day).distinct('order_id')
        total_order_changes = total_order_changes | order_changes
        current_day = previous_day
    for item in total_order_changes:
        order = Order.objects.get(id=item.order_id)
        past_year_value += order.get_total_cost()
    months_list = get_months(today.month)
    year_orders = OrderChange.objects.order_by(
        'order_id').filter(
        date__gte=year_ago).filter(
        final_status='confirmed').distinct(
        'order_id')
    year_orders_per_month = get_orders_per_month(year_orders, months_list)
    two_years_ago = year_ago - datetime.timedelta(days=365)
    last_year_orders = OrderChange.objects.order_by(
        'order_id').filter(
        final_status='confirmed').exclude(
        date__gte=year_ago).filter(
        date__gte=two_years_ago).distinct(
        'order_id')
    last_year_orders_per_month = get_orders_per_month(last_year_orders, months_list)
    year_orders = list(year_orders_per_month.values())
    last_year_orders = list(last_year_orders_per_month.values())
    # Segundo gráfico
    customers = Customer.objects.all()
    customer_dict = create_cust_dict(customers)
    orders = Order.objects.all()
    cust_list = []
    for order in orders:
        customer_name = order.customer.name
    for key in customer_dict:
        for order in orders:
            if key == order.customer.name:
                for k in customer_dict[key]:
                    if k == order.status:
                        customer_dict[key][k] += 1
    orders_per_cust_keys = list(customer_dict.keys())
    orders_per_cust_dicts = list(customer_dict.values())
    closest_orders = Order.objects.order_by('due_date')[:5]
    return render(request, 'account/dashboard.html', {'section': dashboard, 
        'customers': customers, 
        'categories': categories,
        'total_value': total_value,
        'past_year_value': past_year_value,
        'last_year_orders': last_year_orders,
        'year_orders': year_orders,
        'months_list': months_list,
        'closest_orders': closest_orders
        })

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
    actual_month = month - 10
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
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form, 'categories': categories, 'customers': customers})
