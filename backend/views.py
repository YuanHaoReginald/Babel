from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import render, render_to_response, redirect
from django import forms
from django.http import HttpResponse
from django.contrib import messages
from .models import *
import os

# Create your views here.

# translater sign up
def TranslaterSignUp(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        new_telephone = request.POST.get('telephone')
        new_email = request.POST.get('email')
        new_avatarImageUrl = request.POST.get('avatarImageUrl')

        existedTranslater = Translater.objects.filter(username = new_username)

        # fail to sign up because there exists a user
        if(len(existedTranslater) >= 0):
            return HttpResponse(0)

        # succeed and insert
        models.Translater.objects.create(username = new_username,password = new_password, telephone = new_telephone,email = new_email,avatarImageUrl = new_avatarImageUrl )
        existedTranslater = Translater.objects.filter(username = new_username)
        current_translater = existedTranslater[0]
        return HttpResponse(current_translater.id)

# translater login in
def TranslaterSignIn(request):
    if request.method == 'POST':
        current_username = request.GET.get('username')
        current_password = request.GET.get('password')
        existedTranslater = Translater.objects.filter(username=current_username,password = current_password)
        if(len(existedTranslater) == 1):
            # get it
            current_translater = existedTranslater[0]
            return HttpResponse(current_translater.id)
        else:
            return HttpResponse(0)

 # employer sign up
def EmployerSignUp(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        new_telephone = request.POST.get('telephone')
        new_email = request.POST.get('email')
        new_avatarImageUrl = request.POST.get('avatarImageUrl')

        existedEmployer = Employer.objects.filter(username = new_username)

        # fail to sign up because there exists a user
        if(len(existedEmployer) >= 0):
            return HttpResponse(0)

        # succeed and insert
        models.existedEmployer.objects.create(username = new_username,password = new_password, telephone = new_telephone,email = new_email,avatarImageUrl = new_avatarImageUrl )

        existedEmployer = Employer.objects.filter(username=new_username)
        current_employer = existedEmployer[0]
        # return its primary key
        return HttpResponse(current_employer.id)

# Employer login in
def EmployerSignIn(request):
    if request.method == 'POST':
        current_username = request.GET.get('username')
        current_password = request.GET.get('password')
        existedEmployer = Employer.objects.filter(username=current_username,password = current_password)

        if(len(existedEmployer) == 1):
            # get it
            current_employer = existedEmployer[0]
            return HttpResponse(current_employer.id)
        else:
            return HttpResponse(0)