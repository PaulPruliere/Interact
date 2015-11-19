from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime 
from appinteract.forms import ConnexionForm
from django.core.context_processors import csrf
from django.contrib.auth import authenticate , login , logout
import logging
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from subprocess import Popen, PIPE


def connexion(request):

	if request.user.is_active:
		return HttpResponseRedirect('graphe')
	if request.method == "POST" :
		form = ConnexionForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request,user)
					return HttpResponseRedirect('graphe')
	else :
		form = ConnexionForm()
	return render(request,'appinteract/connexion.html', locals())


def deconnexion(request):

	logout(request)
	return redirect(reverse(connexion))


@login_required
def graphe(request):
	outputMichael, error = Popen(["docker", "exec", "paulsapp_fetch_1", "python", "/opt/fetch27/data/dataMichael.py"], stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()
	outputSeb, error = Popen(["docker", "exec", "paulsapp_fetch_1", "python", "/opt/fetch27/data/dataSeb.py"], stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()
	jsonMichael = outputMichael
	jsonSeb = outputSeb
	return render(request, 'appinteract/grapheOK.html', locals())