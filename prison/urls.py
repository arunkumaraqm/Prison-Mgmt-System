from django.urls import path
from . import views

app_name = 'prison'
urlpatterns = [
	# path(route, view, kwargs, name) is the format

	path('', views.index, name='home'),
	path('show', views.show, name='show'),
	path('insert', views.insert, name='insert'),
	path('destroy/<int:prisoner_id>', views.destroy, name='destroy'),
	path('edit/<int:prisoner_id>', views.edit, name='edit'),

	path('<int:prisoner_id>/visitors', views.show_visitors, name='visitors'),
	path('<int:prisoner_id>/visitors/<int:visitor_id>/remove', views.remove_visitor_from_prisoner, name='remove_visitor_from_prisoner'),
	path('<int:prisoner_id>/visitors/insert', views.insert_visitor_to_prisoner, name='insert_visitor_to_prisoner'),
]