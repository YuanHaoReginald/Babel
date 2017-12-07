from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import *
from Babel import settings

import os
import json
from urllib.parse import urljoin
import datetime

# Create your views here.

# user signup
def UserSignUp(request):
    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
        new_username = info_dict['username']
        new_password = info_dict['password']
        new_email = info_dict['email']
        user_type = info_dict['utype']
        try:
            existedUser = User.objects.get(username=new_username)
            response_dict = {'id': 0}
        except:
            if user_type == 'translator':
                new_user = Translator.objects.create_user(username=new_username, password=new_password, email=new_email, utype='translator')
            elif user_type == 'employer':
                new_user = Employer.objects.create_user(username=new_username, password=new_password, email=new_email, utype='employer')
            response_dict = {'id': new_user.id}
        login(request, new_user)
        return JsonResponse(response_dict)


# user login
def UserSignIn(request):
    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
        username = info_dict['username']
        password = info_dict['password']
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'id': 0})
        else:
            login(request, user)
            return JsonResponse({'id': user.id, 'utype': user.utype})

# get user info
@login_required
def GetUserInfo(request):
    if request.method == 'GET':
        user = auth.get_user(request)
        if user.utype == 'translator':
            user = user.translator
        elif user.utype == 'employer':
            user = user.employer
        response_dict = {'username': user.username,
                         'email': user.email,
                         'headSrc': '',
                         'level': user.creditLevel,
                         'experience': user.experience}
        if user.avatar:
            response_dict['headSrc'] = user.avatar.url
        return JsonResponse(response_dict)


# sign up more
def UserModify(request):
    user = auth.get_user(request)
    if user.utype == 'translator':
        user = user.translator
    elif user.utype == 'employer':
        user = user.employer
    if request.method == 'POST':
        try:
            info_dict = json.loads(request.body.decode())
            user.telephone = info_dict['telephone']
            user.alipayNumber = info_dict['alipayNumber']
            user.wechatNumber = info_dict['wechatNumber']
            user.save()
            return JsonResponse({'status': True})
        except:
            return JsonResponse({'status': False})
    elif request.method == 'GET':
        response_dict = {'telephone': user.telephone,
                         'wechatNumber': user.wechatNumber,
                         'alipayNumber': user.alipayNumber,
                         'language': 'French',
                         'avatar': user.avatar.url}
        return JsonResponse(response_dict)

def UploadAvatar(request):
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        user = auth.get_user(request)
        file_extension = avatar.name.split('.')[-1]
        user.avatar.delete()
        user.avatar.save(user.username + '.' + file_extension, avatar)
    return JsonResponse({'url': user.avatar.name})

def CreateTask(request):
    user = auth.get_user(request).employer
    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
        print(info_dict)
        task_title = info_dict['title']
        task_description = info_dict['description']
        task_language = info_dict['language']
        task_license = info_dict['license']
        task_level = info_dict['level']
        task_tags = info_dict['tags']
        task_ddlTime = info_dict['ddlTime']
        task_assignments = info_dict['assignments']
        task = Task.objects.create(title = task_title,
                                   description = task_description,
                                   fileType = 0,
                                   employer = user,
                                   ddlTime = task_ddlTime,
                                   languageTarget = 3,
                                   requirementCreditLevel = task_level)
        print('task')
        for assignment in task_assignments:
            Assignment.objects.create(task = task,
                                      order = assignment['order'],
                                      description = assignment['text'])
        return JsonResponse({'task_id': task.id})

def UploadTaskFile(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        taskid = request.POST.get('id')
        task = Task.objects.get(id = taskid)
        task.fileUrl.save(file)
    return HttpResponse(0)

def GetEmployerTasks(request):
    if request.method == 'GET':
        print('-----------------------GetEmployerTasks-----------------')
        current_user = auth.get_user(request).employer
        task_set = current_user.task_set.all()
        response_dict = {'taskList': []}
        for task in task_set:
            _task_tag = task.tag_set.all()
            _temp_tag_list = []
            for tag in _task_tag:
                _temp_tag_list.append(tag)
            response_dict['taskList'].append({
                'title': task.title,
                'publishTime': task.publishTime.timestamp(),
                'ddlTime': task.ddlTime.timestamp(),
                'tags': _temp_tag_list,
                'language': task.languageOrigin if task.languageOrigin == 0 else task.languageTarget,
                'description': task.description,
            })
        return JsonResponse(response_dict)
