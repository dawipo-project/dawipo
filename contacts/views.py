from django.shortcuts import render
from .forms import ContactForm
from .models import Contact

def landing_view(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			contact = form.save()
			return render(request, 'index.html')
	form = ContactForm()
	return render(request, 'index.html', {'form': form})

def quienes_somos(request):
	return render(request, 'team.html')