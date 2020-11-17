from django.http import HttpResponse
from django.shortcuts import redirect

NOT_AUTHORIZED_MESSAGE = "You are not authorized to view this page."

def my_login_required(view_func):
	def wrapper(request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('/')
		else:
			return view_func(request, *args, **kwargs)
	return wrapper

def allowed_users(allowed_roles = None):
	if allowed_roles is None: 
		allowed_roles = []

	def decorator(view_func):
		def wrapper(request, *args, **kwargs):
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name # assuming user is only in one group
			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse(NOT_AUTHORIZED_MESSAGE)
		return wrapper
	return decorator	