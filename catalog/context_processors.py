# from .models import Category
# from django.contrib.auth.decorators import login_required

# @login_required
# def categories(request):
# 	categories = {' ': None}
# 	if request.user.is_authenticated:
# 		categories = Category.objects.filter(company=request.user.profile.company)
# 		return {'categories': categories}
# 	return categories