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
        new_email = info_dict['email']

        existedTranslator = Translator.objects.filter(username = new_username)

        # fail to sign up because there exists a user
        if(len(existedTranslator) >= 1):
            response_dict = {'id':0}
        else: # succeed and insert
            translator = Translator.objects.create(username = new_username, password = new_password, email = new_email)
            response_dict = {'id': translator.id}
        return JsonResponse(response_dict)

# employer sign up
def EmployerSignUp(request):
    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
        new_username = info_dict['username']
        new_password = info_dict['password']
        new_email = info_dict['email']

        existedEmployer = Employer.objects.filter(username=new_username)
        # fail to sign up because there exists a user
        if (len(existedEmployer) >= 1):
            response_dict = {'id': 0}
        else:  # succeed and insert
            employer = Employer.objects.create(username=new_username, password=new_password, email=new_email)
            response_dict = {'id': employer.id}
        return JsonResponse(response_dict)

# a comomn sign up
def UserSignUp(request):

    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
        new_username = info_dict['username']
        new_password = info_dict['password']
        new_email = info_dict['email']
        user_type = info_dict['utype']
        existedUser = CommonUser.objects.filter(username = new_username)
        if(len(existedUser) == 1):
            # get it
            response_dict = {'id': 0}
        else:
            if(user_type == 'Translater'):
                new_user = Translator.objects.create( username = new_username, password = new_password, email = new_email,  utype = user_type)
                response_dict = {'id': new_user.id }
            elif(user_type == 'Employer'):
                new_user = Employer.objects.create( username = new_username, password = new_password, email = new_email,  utype = user_type)
                response_dict = {'id' : new_user.id}
            else:
                response_dict = {'id': 0}
        return JsonResponse(response_dict)


# translator login in
def UserSignIn(request):
    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
        current_username = info_dict['username']
        current_password = info_dict['password']
        existedUser = CommonUser.objects.filter(username = current_username,password = current_password)
        if(len(existedUser) == 1):
            # get it
            current_user = existedUser[0]
            response_dict = {'id': current_user.id, 'utype' :current_user.utype }
            return JsonResponse(response_dict)
        else:
            response_dict = {'id': 0}
            return JsonResponse(response_dict)

# get user info
def GetUserInfo(request):
    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
        user_id = info_dict['id']
        # response_dict =
        existedUser = CommonUser.objects.filter(id = user_id)

        if(len(existedUser) == 1):
            # get it
            current_user = existedUser[0]
            response_dict = {'id': current_user.id, 'username':current_user.username,'email':current_user.email, 'headSrc':current_user.avatarImageUrl}
            return JsonResponse(response_dict)
        else:
            response_dict = {'id':0 }
            return JsonResponse(response_dict)
        return

# get


