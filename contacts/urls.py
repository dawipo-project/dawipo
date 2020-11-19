from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
	path('', views.landing_view, name='landing_view'),
]