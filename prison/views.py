from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .models import Prisoner as Pr, Visitor
from .forms import *
from accounts.decorators import my_login_required, allowed_users

@my_login_required
def index(request):
	is_police = False
	is_neither = False

	if request.user.groups.exists():
		# Assuming user is only in one group
		if 'Police' == request.user.groups.all()[0].name: 
			is_police = True
	else:
		is_neither = True

	return render(
		request, 
		'prison/index.html', 
		{'is_police': is_police, 'is_neither': is_neither}
		)

@my_login_required
@allowed_users(['DataManager', 'Police'])
def show(request):
	prisoners = Pr.objects.all()
	is_datamanager = (request.user.groups.all()[0].name == 'DataManager') # Only DM should be able to view certain options

	return render(
		request, 
		'prison/show.html', 
		{'prisoners': prisoners, 'is_datamanager': is_datamanager}
		)

@my_login_required
@allowed_users(['DataManager'])
def insert(request):
	if request.method == 'GET':
		form = PrisonerForm()

	elif request.method == 'POST':
		form = PrisonerForm(request.POST)
		if form.is_valid():
			form.save() 
			return redirect('prison:show')

	return render(
		request,
		'prison/insert.html',
		{'form': form}
		)

@my_login_required
@allowed_users(['DataManager'])
def destroy(request, prisoner_id):
	prisoner = get_object_or_404(Pr, id=prisoner_id)

	if request.method == 'GET':
		return render(
			request,
			'prison/delete.html',
			{'prisoner': prisoner}
			)
	elif request.method == 'POST':
		prisoner.delete()
		#TODO Confirm delete
		#TODO Remove visitors from the prisoner before deleting prisoner
		return redirect('prison:show')

@my_login_required
@allowed_users(['DataManager'])
def edit(request, prisoner_id):
	prisoner = get_object_or_404(Pr, id=prisoner_id)
	form = PrisonerForm(request.POST or None, instance = prisoner)

	if request.method == 'POST':
		if form.is_valid():
			form.save() 
			return redirect('prison:show')

	return render(
		request,
		'prison/edit.html',
		{'prisoner': prisoner, 'form': form}
	)


@my_login_required
@allowed_users(['Police', 'DataManager'])
def show_visitors(request, prisoner_id):
	'''
	If you go to the url /prison/destroy/10, then
	the prisoner with id 10 will be deleted
	and you will be redirected to /prison/show
	'''

	prisoner = get_object_or_404(Pr, id=prisoner_id)
	visitors = prisoner.visitor_set.all()

	is_datamanager = (request.user.groups.all()[0].name == 'DataManager')

	return render(
		request,
		'prison/show_visitors.html',
		{'prisoner': prisoner, 'visitors': visitors, 'is_datamanager': is_datamanager}
	)

	
@my_login_required
@allowed_users(['DataManager'])
def insert_visitor_to_prisoner(request, prisoner_id):

	prisoner = get_object_or_404(Pr, id=prisoner_id)

	inapplicable_visitors = prisoner.visitor_set.all()
	applicable_visitors = Visitor.objects.exclude(visitor_id__in=inapplicable_visitors)
	ev_form = ExistingVisitorForm(applicable_visitors, request.POST or None)
	
	nv_form = NewVisitorForm(request.POST or None)
	
	if request.method == 'POST':
		if ev_form.is_valid():
			visitor = ev_form.cleaned_data['visitor']
			visitor.associated_prisoners.add(prisoner)
			visitor.save()
		elif nv_form.is_valid():
			nv_form.save(commit=True, default_associated_prisoner=prisoner)
			
		return redirect('prison:visitors', prisoner_id)

	return render(
		request,
		'prison/insert_visitor_to_prisoner.html',
		{'prisoner': prisoner, 'ev_form': ev_form, 'nv_form': nv_form}
	)
	
@my_login_required
@allowed_users(['DataManager'])
def remove_visitor_from_prisoner(request, prisoner_id, visitor_id):
	'''
	Given a prisoner and a visitor who visits that prisoner, 
	dissociate both of them and delete the visitor if they do not visit any more prisoners.
	'''

	prisoner = get_object_or_404(Pr, id=prisoner_id)

	# In case visitor doesn't actually visit the prisoner
	try:
		visitor = prisoner.visitor_set.get(visitor_id=visitor_id)
	except Visitor.DoesNotExist:
		raise Http404('Visitor and prisoner did not match.')
	
	if request.method == 'GET':
		return render(
			request,
			'prison/remove_visitor_from_prisoner.html',
			{'prisoner':prisoner, 'visitor':visitor,}
			)
	elif request.method == 'POST':
		# Dissociate visitor and prisoner
		visitor.associated_prisoners.remove(prisoner)
		visitor.save()

		# Delete visitor if visitor is not connected to any prisoner
		if not visitor.associated_prisoners.all():
			visitor.delete()

		# return HttpResponseRedirect(reverse('prison:visitors', prisoner_id))
		return redirect('prison:visitors', prisoner_id)
