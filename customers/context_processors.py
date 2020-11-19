from .models import Customer
from django.contrib.auth.decorators import login_required

@login_required
def customers(request):
	customers = {}
	if request.user.is_authenticated:
		customers = Customer.objects.filter(company=request.user.profile.company)
		return {'customers': customers}
	return customers