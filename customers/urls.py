from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
	path('export_csv/', views.export_csv, name='export_csv'),
	path('create/', views.CustomerRegistrationView.as_view(), name='customer_registration'),
	path('list/', views.CustomerList.as_view(), name='customer_list'),
	path('<int:pk>/', views.CustomerDetail.as_view(), name='cust_detail'),
	path('import/', views.import_csv, name='import_csv'),
]