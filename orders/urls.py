from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
	path('product_list/', views.product_list, name='orders_product_list'),
	path('product_list/<slug:category_slug>', views.product_list, name='orders_product_list_by_category'),
	path('edit/<int:order_id>/', views.order_edit, name='order_edit'),
	path('order_items/edit/<pk>/', views.UpdateOrderItem.as_view(), name='order_item_edit'),
	path('create/', views.order_create, name='order_create'),
	path('list/', views.OrderList.as_view(), name='order_list'),
	path('<int:order_id>/detail/', views.order_detail, name='order_detail'),
	path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
	path('download/<int:order_id>/', views.download_order_pdf, name='get_pdf'),
]