from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .models import Prisoner as Pr

class IndexView(generic.ListView):
	template_name = 'prison/index.html'
	context_object_name = 'new_prisoners_list'

	def get_queryset(self):
		return Pr.objects.order_by('start_date')[:10]

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