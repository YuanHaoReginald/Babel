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

# user signup
def UserSignUp(request):

    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
        new_username = info_dict['username']
        new_password = info_dict['password']
        new_email = info_dict['email']
        user_type = info_dict['utype']
        print(user_type)
        existedUser = CommonUser.objects.filter(username = new_username)
        if(len(existedUser) == 1):
            # get it
            response_dict = {'id': 0}
        else:
            if (user_type == 'translator'):
                new_user = Translator.objects.create(username = new_username, password = new_password, email = new_email,  utype = user_type)
                response_dict = {'id': new_user.id }
            elif (user_type == 'employer'):
                new_user = Employer.objects.create(username = new_username, password = new_password, email = new_email,  utype = user_type)
                response_dict = {'id' : new_user.id}
            else:
                response_dict = {'id': 0}
        return JsonResponse(response_dict)


# user login
def UserSignIn(request):
    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
        current_username = info_dict['username']
        current_password = info_dict['password']
        print(info_dict)
        existedUser = CommonUser.objects.filter(username = current_username,password = current_password)
        print(existedUser)
        if(len(existedUser) == 1):
            # get it
            current_user = existedUser[0]
            response_dict = {'id': current_user.id, 'utype': current_user.utype }
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
            response_dict = {'id': current_user.id, 'username':current_user.username,'email':current_user.email, 'headSrc':current_user.avatar}
            return JsonResponse(response_dict)
        else:
            response_dict = {'id':0 }
            return JsonResponse(response_dict)

# sign up more
def UserModify(request):
    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())

        user_id =  info_dict['id']

        user_telephone = info_dict['telephone']
        user_alipay = info_dict['alipayNumber']
        user_wechat = info_dict['wechatNumber']
        user_language = info_dict['language']

        existedUser = CommonUser.objects.filter(user_id)

        if(len(existedUser) == 1):
            # get it
            # change the user information
            current_user = existedUser[0]
            current_user.telephone = user_telephone
            current_user.alipayNumber = user_alipay
            current_user.wechatNumber = user_wechat
            current_user.save()
            # language
            Language.objects.create(languageType = user_language, TranslatorId = current_user)
            
            response_dict = {'status': True}
        else:
            response_dict = {'status': False}

        return JsonResponse(response_dict)

def UploadAvatar(request):
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        print(avatar)
        print(request.POST.get('a'))
    return HttpResponse(0)
