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
            existedUser = CommonUser.objects.get(username = new_username)
            response_dict = {'id': 0}
        except:
            if (user_type == 'translator'):
                new_user = Translator.objects.create(username = new_username, password = new_password, email = new_email, utype = user_type)
                response_dict = {'id': new_user.id}
            elif (user_type == 'employer'):
                new_user = Employer.objects.create(username = new_username, password = new_password, email = new_email, utype = user_type)
                response_dict = {'id': new_user.id}
        return JsonResponse(response_dict)


# user login
def UserSignIn(request):
    if request.method == 'POST':
        print('login~~~~~~')
        info_dict = json.loads(request.body.decode())
        username = info_dict['username']
        password = info_dict['password']
        user = authenticate(username=username, password=password)
        if user == None:
            print(0)
            return JsonResponse({'id': 0})
        else:
            print(1)
            login(request, user)
            myuser = CommonUser.objects.get(username=username)
            return JsonResponse({'id': user.id, 'utype': myuser.utype })

# get user info
@login_required
def GetUserInfo(request):
    if request.method == 'GET':
        # response_dict =
        user = auth.get_user(request)
        response_dict = {'id': user.id,
                         'username': user.username,
                         'email': user.email,
                         'headSrc': '',
                         'level': user.level,
                         'experience': user.experience}
        if user.avatar:
            response_dict['headSrc'] = urljoin(settings.CONFIGS['SITE_DOMAIN'], os.path.join(settings.MEDIA_URL, name))
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
    elif request.method == 'GET':
        current_user = auth.get_user(request)
        response_dict = {'telephone': current_user.telephone,
                         'wechatNumber': current_user.wechatNumber,
                         'alipayNumber': current_user.alipayNumber,
                         'language': 'French',
                         'avatar': current_user.avatar}
        return JsonResponse(response_dict)


    

def UploadAvatar(request):
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        userid = request.POST.get('id')
        current_user = CommonUser.objects.get(id=userid)
        file_extension = avatar.name.split('.')[-1]
        current_user.avatar.save(userid + '.' + file_extension, avatar)
    return HttpResponse(current_user.avatar)

def CreateTask(request):
    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
        print(info_dict)
        task_title = info_dict['title']
        task_description = info_dict['description']
        task_language = info_dict['language']
        task_license = info_dict['license']
        task_tags = info_dict['tags']
        task_assignments = info_dict['assignments']
        Task.objects.create(title = task_title, description = task_description)
    return HttpResponse()

def UploadTaskFile(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        taskid = request.POST.get('id')
        task = Task.objects.get(id = taskid)
        task.fileUrl.save(file)
    return HttpResponse(0)