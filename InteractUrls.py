from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns =[
	url(r'^graphe$', views.graphe , name='graphe'),
	url(r'^connexion$', views.connexion , name='connexion'),
	url(r'^deconnexion$', login_required(views.deconnexion) , name='deconnexion'),
]