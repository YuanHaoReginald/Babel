from django.shortcuts import render
from django.contrib import auth
from django.shortcuts import render, render_to_response, redirect
from django import forms
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from django.core import serializers

import os
import json
import time

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

# add task vue : Add task
def AddTask(request):
    info_dict = json.loads(request.body.decode())
    task_title = info_dict['title']
    task_language = info_dict['language']
    task_description = info_dict['description']
    task_fileurl = info_dict['fileurl']
    task_filename = info_dict['file_name']

    name_list = task_filename.split('.',1)
    name_suffix = name_list[-1]
    text_suffix_list = ['doc','docx','txt','md']
    if name_suffix in text_suffix_list:
        task_fileType = 0
    else:
        task_fileType = 1

    task_publishTime = time.time()
    task_ddlTime = time.time() + 24 * 3600 * 30

    try:
        Task.objects.create(title = task_title, description = task_description, fileUrl = task_fileurl, fileType = task_fileType, language = task_language,
                        publishTime = task_publishTime, ddlTime = task_ddlTime)
        return HttpResponse(1)
    except:
        return HttpResponse(0)

# show task list: Tasks
def ShowTaskList(request):
    if request.method == 'POST':
        json_all_tasks = serializers.serialize("json", Task.objects.all())
        return HttpResponse(json_all_tasks)

# show a task: TaskPage
def ShowSingleTask(request):
    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
        task_id = info_dict['id']
        json_task =  serializers.serialize("json", Task.objects.get(id = task_id))
        return HttpResponse(json_task)

# s
