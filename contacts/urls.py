from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
	path('', views.landing_view, name='landing_view'),
	path('quienes_somos', views.quienes_somos, name='quienes_somos'),
]