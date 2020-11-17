from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Prisoner as Pr
from .forms import PrisonerForm
from accounts.decorators import my_login_required, allowed_users

@my_login_required
def index(request):
	is_police = False
	is_neither = False

	if request.user.groups.exists():
		if 'Police' == request.user.groups.all()[0].name: # Assuming user is only in one group
			is_police = True
	else:
		is_neither = True

	return render(
		request, 
		"prison/index.html", 
		{'is_police': is_police, 'is_neither': is_neither}
		)
	
@my_login_required
@allowed_users(['Police'])
def plainshow(request):
	prisoners = Pr.objects.all()
	return render(
		request, 
		"prison/plainshow.html", 
		{'prisoners': prisoners}
		)

@my_login_required
@allowed_users(['DataManager'])
def show(request):
	prisoners = Pr.objects.all()
	return render(
		request, 
		"prison/show.html", 
		{'prisoners': prisoners}
		)

@my_login_required
@allowed_users(['DataManager'])
def insert(request):
	if request.method == "GET":
		form = PrisonerForm()

	elif request.method == "POST":
		form = PrisonerForm(request.POST)
		if form.is_valid():
			form.save() 
			return redirect(show)

	return render(
		request,
		'prison/insert.html',
		{'form': form}
		)

@my_login_required
@allowed_users(['DataManager'])
def destroy(request, id):
	# If you go to the url /prison/destroy/10, then
	# the prisoner with id 10 will be deleted
	# and you will be redirected to /prison/show
	prisoner = get_object_or_404(Pr, id=id)
	prisoner.delete()
	return redirect(show)

@my_login_required
@allowed_users(['DataManager'])
def edit(request, id):
	prisoner = get_object_or_404(Pr, id=id)
	form = PrisonerForm(request.POST or None, instance = prisoner)

	if request.method == "POST":
		print("LOG: ", prisoner.start_date)
		if form.is_valid():
			form.save() 
			return redirect(show)

	return render(
		request,
		'prison/edit.html',
		{'prisoner': prisoner, 'form': form}
		)

# class DetailView(generic.DetailView):
# 	model = Pr
# 	template_name = 'prisoner/details.html'

# class ResultsView(generic.DetailView):
# 	model = Pr
# 	template_name = 'prisoner/results.html'

# def vote(request, prisoner_id):
#     prisoner = get_object_or_404(Pr, pk=prisoner_id)
#     try:
#         selected_choice = prisoner.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Ch.DoesNotExist):
#         # Redisplay the prisoner voting form.
#         return render(request, 'prisoner/detail.html', {
#             'prisoner': prisoner,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes += 1
#         selected_choice.save()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('results', args=(prisoner.id,)))