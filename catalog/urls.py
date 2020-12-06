from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
	path('catalog/export_csv/', views.export_csv, name='export_all_csv'),
	path('catalog/list/', views.ProductList.as_view(), name='product_list_table'),
	# path('catalog/add/', views.ProductCreate.as_view(), name='add_product'),
	path('catalog/add/', views.create_product, name='add_product'),
	path('catalog/category/add/', views.CategoryCreate.as_view(), name='add_category'),
	path('catalog/', views.product_list, name='product_list'),
	path('catalog/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
	path('catalog/<slug>/list/', views.CategoryProductList.as_view(), name='category_product_list_table'),
	path('catalog/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
	path('catalog/<int:id>/<slug:slug>/edit/', views.edit, name='product_edit'),
]