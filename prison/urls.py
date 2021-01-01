from django.urls import path
from . import views

urlpatterns = [
	# path(route, view, kwargs, name) is the format

	path('', views.index, name = "Home"),
	path('show', views.show, name = "Show"),
	path('insert', views.insert, name = "Insert"),
	path('destroy/<int:id>', views.destroy),
	path('edit/<int:id>', views.edit),

	path('<int:id>/visitor/', views.show_visitors),
	path('<int:prisoner_id>/visitor/<int:visitor_id>/remove', views.remove_visitor_from_prisoner),
	path('<int:prisoner_id>/visitor/insert', views.insert_visitor_to_prisoner),
]