from django.urls import path
from . import views

urlpatterns = [
	#path(route, view, kwargs, name)
	path('', views.index, name = "Home"),
	path('plainshow', views.plainshow, name = "Show"),
	path('show', views.show, name = "Show"),
	path('insert', views.insert, name = "Insert"),
	path('destroy/<int:id>', views.destroy),
	path('edit/<int:id>', views.edit),
	# path('<int:id>/visitor/add', views.add_visitor),
	path('<int:id>/visitor/', views.show_visitors),
	path('<int:prisoner_id>/visitor/<int:visitor_id>/remove', views.remove_visitor_from_prisoner),
	path('<int:prisoner_id>/visitor/insert', views.insert_visitor_to_prisoner),
	# path('<int:pk>/', views.DetailView.as_view(), name = "detail"),
]