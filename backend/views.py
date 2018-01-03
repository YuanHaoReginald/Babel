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
        assignment.status = 2
        assignment.save()
        return JsonResponse({'status': True})
    
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
                'id': assignment.id,
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
                    'translator': assignment.translator.username if assignment.translator else '',
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


def SolveDispute(request):
    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
        dispute_id = info_dict['disputeid']
        result = info_dict['result']
        statement = info_dict['statement']
        dispute = Dispute.objects.get(id=dispute_id)
        dispute.adminStatement = statement
        if result:
            dispute.status = 1
        else:
            dispute.status = 2
        dispute.save()
        return JsonResponse({'status': True})

def VerifyLicense(request):
    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
        license_id = info_dict['licenseid']
        result = info_dict['result']
        license = License.objects.get(id=license_id)
        if result:
            license.adminVerify = 1
        else:
            license.adminVerify = 2
        license.save()
        return JsonResponse({'status': True})

def GetManager(request):
    if request.method == 'GET':
        print('-----------------------GetManager-----------------')
        response_dict = {
            'DisputeList': [],
            'LicenseList': []
        }
        dispute_set = Dispute.objects.filter(status=0)
        if dispute_set.count() > 100:
            dispute_set = dispute_set[:100]
        for dispute in dispute_set:
            response_dict['DisputeList'].append({
                'id': dispute.id,
                'assignment_name': dispute.assignment.description,
                'argument_translator': dispute.translatorStatement,
                'argument_employer': dispute.employerStatement,
            })
        license_set = License.objects.filter(status=0)
        if license_set.count() > 100:
            license_set = license_set[:100]
        for _license in license_set:
            response_dict['LicenseList'].append({
                'id': _license.id,
                'type': _license.licenseType,
                'description': _license.description,
                'url': _license.licenseImage,
            })
        return JsonResponse(response_dict)

def AcceptAssignment(request):
    if request.method == 'POST':
        info_dict = json.loads(request.body.decode())
        assignment_id = info_dict['assignmentid']
        result = info_dict['result']
        acceptance = info_dict['acceptance']
        assignment = Assignment.objects.get(id=assignment_id)
        if acceptance == 'accept':
            assignment.scores = result
        elif acceptance == 'reject':
            Dispute.objects.create(assignment=assignment_id, employerStatement=result)
        assignment.status = 3
        assignment.save()
        return JsonResponse({'status': True})
