from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import render, render_to_response, redirect
from django import forms
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from .models import *

import os
import json


# Create your views here.
# translator sign up
def TranslatorSignUp(request):

    if request.method == 'POST':

        info_dict = json.loads(request.body.decode())
        new_username = info_dict['username']
        new_password = info_dict['password']
        new_avatarImageUrl = info_dict['avatarImageUrl']

        existedTranslator = Translator.objects.filter(username = new_username)

        # fail to sign up because there exists a user
        if(len(existedTranslator) >= 1):
            response_dict = {'id':0}
        elif: # succeed and insert
            translator = Translator.objects.create(username = new_username, password = new_password, email = new_email)
            response_dict = {'id': translator.id}
        return JsonResponse(response_dict)

# translator login in
def TranslatorSignIn(request):

    if request.method == 'POST':

        info_dict = json.loads(request.body.decode())
        current_username = info_dict['username']
        current_password = info_dict['password']

        existedTranslator = Translator.objects.filter(username=current_username,password = current_password)
        if(len(existedTranslator) == 1):
            # get it
            current_translator = existedTranslator[0]
            response_dict = {'id': current_translator.id}
            return JsonResponse(response_dict)
        else:
            response_dict = {'id': 0}
            return JsonResponse(response_dict)

# employer sign up
def EmployerSignUp(request):

    if request.method == 'POST':

        info_dict = json.loads(request.body.decode())
        new_username = info_dict['username']
        new_password = info_dict['password']
        new_email = info_dict['email']

        existedEmployer = Employer.objects.filter(username = new_username)

        # fail to sign up because there exists a user
        if( len(existedEmployer) >= 1 ):
            response_dict = {'id': 0}
        elif: # succeed and insert
            employer = Employer.objects.create(username = new_username,password = new_password, email = new_email)
            response_dict = {'id': employer.id}
        return JsonResponse(response_dict)

# Employer login in
def EmployerSignIn(request):
    
    if request.method == 'POST':

        info_dict = json.loads(request.body.decode())
        current_username = info_dict['username']
        current_password = info_dict['password']

        existedEmployer = Employer.objects.filter(username=current_username,password = current_password)

        if(len(existedEmployer) == 1):
            # get it
            current_employer = existedEmployer[0]
            response_dict = {'id': current_employer.id}
            return JsonResponse(response_dict)
        else:
            response_dict = {'id':0}
            return JsonResponse(response_dict)
