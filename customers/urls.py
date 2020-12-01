from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
	path('create/', views.CustomerRegistrationView.as_view(), name='customer_registration'),
	path('list/', views.CustomerList.as_view(), name='customer_list'),
	path('import/', views.import_csv, name='import_csv'),
]