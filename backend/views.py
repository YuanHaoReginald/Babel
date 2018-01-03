from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import *
from django.core import serializers
import datetime

import os
import json
import time
from Babel import settings
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
            existedUser = User.objects.get(username=new_username)
            response_dict = {'id': 0}
        except:
            if user_type == 'translator':
                new_user = Translator.objects.create_user(username=new_username, password=new_password, email=new_email, utype='translator')
            elif user_type == 'employer':
                new_user = Employer.objects.create_user(username=new_username, password=new_password, email=new_email, utype='employer')
            response_dict = {'id': new_user.id}
            auth.login(request, new_user)
        return JsonResponse(response_dict)


# user login
def UserSignIn(request):
    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
        username = info_dict['username']
        password = info_dict['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'id': 0})
        else:
            auth.login(request, user)
            return JsonResponse({'id': user.id, 'utype': user.utype})


def UsernameCheck(request):
    if request.method == 'POST':
        username = json.loads(request.body.decode())['username']
        try:
            user = User.objects.get(username=username)
            return JsonResponse({'status': True})
        except:
            return JsonResponse({'status': False})

def UserLogout(request):
    auth.logout(request)
    return HttpResponse(0)

# get user info
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

##### 18/1/2 2:18 ###

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
                         'avatar': user.avatar.url if user.avatar else ''}
        return JsonResponse(response_dict)

# not finish this function
def UploadAvatar(request):
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        user = auth.get_user(request)
        file_extension = avatar.name.split('.')[-1]
        user.avatar.delete()
        user.avatar.save('avatars/' + user.username + '.' + file_extension, avatar)
    return JsonResponse({'url': user.avatar.name})

def CreateTask(request):
    user = auth.get_user(request).employer
    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
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
                                   ddlTime = datetime.datetime.utcfromtimestamp(task_ddlTime),
                                   languageTarget = 3,
                                   requirementCreditLevel = task_level)
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
        task.fileUrl.save('tasks/' + file.name, file)
        print(55)
    return JsonResponse({'url': task.fileUrl.name})


def GetEmployerTasks(request):
    if request.method == 'GET':
        current_user = auth.get_user(request).employer
        task_set = current_user.task_set.all()
        response_dict = {'taskList': []}
        for task in task_set:
            _task_tag = task.tag_set.all()
            _temp_tag_list = []
            for tag in _task_tag:
                _temp_tag_list.append(tag)
            response_dict['taskList'].append({
                'id': task.id,                
                'title': task.title,
                'status': task.status,
                'publishTime': task.publishTime.timestamp(),
                'ddlTime': task.ddlTime.timestamp(),
                'tags': _temp_tag_list,
                'language': task.languageOrigin if task.languageOrigin == 0 else task.languageTarget,
                'description': task.description,
            })
        return JsonResponse(response_dict)

def GetTranslatorAssignments(request):
    if request.method == 'GET':
        current_user = auth.get_user(request).translator
        assignment_set = current_user.assignment_set.all()
        response_dict = {'assignmentList': []}
        for assignment in assignment_set:
            task = assignment.task
            _task_tag = task.tag_set.all()
            _temp_tag_list = []
            for tag in _task_tag:
                _temp_tag_list.append(tag)
            response_dict['assignmentList'].append({
                'id': assignment.id,
                'status': assignment.status,
                'title': task.title,
                'publishTime': task.publishTime.timestamp(),
                'ddlTime': task.ddlTime.timestamp(),
                'tags': _temp_tag_list,
                'language': task.languageOrigin if task.languageOrigin == 0 else task.languageTarget,
                'description': assignment.description,
            })
        return JsonResponse(response_dict)

def PickupAssignment(request):
    if request.method == 'POST':
        user = auth.get_user(request).translator
        info_dict = json.loads(request.body.decode())
        task_id = info_dict['task_id']
        assignment_order = info_dict['assignment_order']
        task = Task.objects.get(id = task_id)
        assignment = Assignment.objects.get(task = task, order = assignment_order)
        assignment.translator = user
        assignment.status = 1
        assignment.save()
        return HttpResponse(0)
    
def GetTaskDetail(request):
    if request.method == 'GET':
        print('-----------------------GetTaskDetail-----------------')
        taskid = request.GET.get('taskid')
        task = Task.objects.get(id=taskid)
        response_dict = {
            'title': task.title,
            'status': task.status,
            'description': task.description,
            'publishTime': task.publishTime.timestamp(),
            'ddlTime': task.ddlTime.timestamp(),
            'language': task.languageOrigin if task.languageOrigin == 0 else task.languageTarget,
            'assignment': []
        }
        assignment_set = task.assignment_set.all()
        for assignment in assignment_set:
            response_dict['assignment'].append({
                'order': assignment.order,
                'description': assignment.description,
                'translator': assignment.translator.username if assignment.translator else '',
                'status': assignment.status,
                'score': assignment.scores,
                'price': assignment.price,
                'submission': assignment.submission.url if assignment.submission else '',
            })
        return JsonResponse(response_dict)

def GetAssignmentDetail(request):
    if request.method == 'GET':
        print('-----------------------GetAssignmentDetail-----------------')
        assignmentid = request.GET.get('assignmentid')
        assignment = Assignment.objects.get(id=assignmentid)
        task = assignment.task
        response_dict = {
            'title': task.title,
            'description': task.description,
            'publishTime': task.publishTime.timestamp(),
            'ddlTime': task.ddlTime.timestamp(),
            'language': task.languageOrigin if task.languageOrigin == 0 else task.languageTarget,
            'assignment': {
                'description': assignment.description,
                'translator': assignment.translator.username if assignment.translator else '',
                'status': assignment.status,
                'score': assignment.scores,
                'price': assignment.price,
                'submission': assignment.submission.name if assignment.submission else ''
            },
            'owner': {
                'name': task.employer.username,
                'avatar': task.employer.avatar.url if task.employer.avatar else ''
            }
        }
        return JsonResponse(response_dict)

def GetSquareTasks(request):
    if request.method == 'GET':
        print('-----------------------GetSquareTasks-----------------')
        # current_user = auth.get_user(request).employer
        task_set = Task.objects.order_by('publishTime')
        if task_set.count() > 5:
            task_set = task_set.reverse()[:5]
        response_dict = {'taskList': []}
        for task in task_set:
            _task_tag = task.tag_set.all()
            _temp_tag_list = []
            for tag in _task_tag:
                _temp_tag_list.append(tag)

            assignment_set = task.assignment_set.all()
            _temp_assignment = []
            for assignment in assignment_set:
                _temp_assignment.append({
                    'order': assignment.order,
                    'description': assignment.description,
                    'translator': assignment.translator,
                    'status': assignment.status,
                    'score': assignment.scores,
                    'price': assignment.price,
                    'submission': assignment.submission.url if assignment.submission else '',
                })

            response_dict['taskList'].append({
                'id': task.id,
                'title': task.title,
                'publishTime': task.publishTime.timestamp(),
                'ddlTime': task.ddlTime.timestamp(),
                'tags': _temp_tag_list,
                'language': task.languageOrigin if task.languageOrigin == 0 else task.languageTarget,
                'description': task.description,
                'assignment': _temp_assignment
            })
        return JsonResponse(response_dict)

def SubmitAssignment(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        assignmentid = request.POST.get('assignmentid')
        print(assignmentid)
        assignment = Assignment.objects.get(id = assignmentid)
        assignment.submission.save('assignments/' + file.name, file)
    return JsonResponse({'url': assignment.submission.name})

def PublishTask(request):
    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
        task_id = info_dict['taskid']
        task = Task.objects.get(id=task_id)
        task.status = 1
        task.save()
        assignment_set = task.assignment_set.all()
        for assignment in assignment_set:
            assignment.status = 1
            assignment.save()
        return JsonResponse({'status': True})
