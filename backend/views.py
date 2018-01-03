from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from .models import *
from django.core import serializers
from django.db import transaction
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
        infoDict = json.loads(request.body.decode())
        newUsername = infoDict['username']
        newPassword = infoDict['password']
        newEmail = infoDict['email']
        userType = infoDict['utype']
        try:
            existedUser = User.objects.get(username=newUsername)
            responseDict = {'id': 0}
        except:
            if userType == 'translator':
                newUser = Translator.objects.create_user(username=newUsername, password=newPassword, email=newEmail, utype='translator')
            elif userType == 'employer':
                newUser = Employer.objects.create_user(username=newUsername, password=newPassword, email=newEmail, utype='employer')
            responseDict = {'id': newUser.id}
            auth.login(request, newUser)
        return JsonResponse(responseDict)


# user login
def UserSignIn(request):
    if request.method == 'POST':
        infoDict = json.loads(request.body.decode())
        username = infoDict['username']
        password = infoDict['password']
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
        responseDict = {'username': user.username,
                         'email': user.email,
                         'headSrc': '',
                         'level': user.creditLevel,
                         'experience': user.experience}
        if user.avatar:
            responseDict['headSrc'] = user.avatar.url
        return JsonResponse(responseDict)

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
            infoDict = json.loads(request.body.decode())
            user.telephone = infoDict['telephone']
            user.alipayNumber = infoDict['alipayNumber']
            user.wechatNumber = infoDict['wechatNumber']
            user.save()
            return JsonResponse({'status': True})
        except:
            return JsonResponse({'status': False})
    elif request.method == 'GET':
        responseDict = {'telephone': user.telephone,
                         'wechatNumber': user.wechatNumber,
                         'alipayNumber': user.alipayNumber,
                         'language': 'French',
                         'avatar': user.avatar.url if user.avatar else ''}
        return JsonResponse(responseDict)

def UploadAvatar(request):
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        user = auth.get_user(request)
        fileExtension = avatar.name.split('.')[-1]
        user.avatar.delete()
        user.avatar.save('avatars/' + user.username + '.' + fileExtension, avatar)
    return JsonResponse({'url': user.avatar.name})

def CreateTask(request):
    if request.method == 'POST':
        user = auth.get_user(request).employer
        info_dict = json.loads(request.body.decode())
        print(info_dict)
        task_title = info_dict['title']
        task_description = info_dict['description']
        task_language = info_dict['language']
        if info_dict['license'] == 'cet4':
            task_license = 4
        elif info_dict['license'] == 'cet8':
            task_license = 8
        task_level = info_dict['level']
        task_tags = info_dict['tags']
        task_ddlTime = info_dict['ddlTime']
        task_assignments = info_dict['assignments']
        if info_dict['language'] == 'English':
            task_languageTarget = 1
        elif info_dict['language'] == 'Japanese':
            task_languageTarget = 2
        elif info_dict['language'] == 'French':
            task_languageTarget = 5
        elif info_dict['language'] == 'Russian':
            task_languageTarget = 4
        elif info_dict['language'] == 'Spanish':
            task_languageTarget = 5
        if info_dict['if_test'] == '需要':
            task_testText = info_dict['testText']
        else:
            task_testText = ''
        task = Task.objects.create(title = task_title,
                                   description = task_description,
                                   fileType = 0,
                                   employer = user,
                                   ddlTime = datetime.datetime.utcfromtimestamp(task_ddlTime),
                                   languageTarget = task_languageTarget,
                                   requirementCreditLevel = task_level,
                                   requirementLicense = task_license,
                                   testText = task_testText)
        for assignment in task_assignments:
            Assignment.objects.create(task = task,
                                      order = assignment['order'],
                                      price = assignment['price'],
                                      description = assignment['text'])
        return JsonResponse({'task_id': task.id})

def UploadTaskFile(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        taskId = request.POST.get('id')
        task = Task.objects.get(id = taskId)
        task.fileUrl.save('tasks/' + file.name, file)
        print(55)
    return JsonResponse({'url': task.fileUrl.name})


def GetEmployerTasks(request):
    if request.method == 'GET':
        currentUser = auth.get_user(request).employer
        taskSet = currentUser.task_set.all()
        responseDict = {'taskList': []}
        for task in taskSet:
            _task_tag = task.tag_set.all()
            _temp_tag_list = []
            for tag in _task_tag:
                _temp_tag_list.append(tag)
            responseDict['taskList'].append({
                'id': task.id,                
                'title': task.title,
                'status': task.status,
                'publishTime': task.publishTime.timestamp(),
                'ddlTime': task.ddlTime.timestamp(),
                'tags': _temp_tag_list,
                'language': task.languageOrigin if task.languageOrigin == 0 else task.languageTarget,
                'description': task.description,
            })
        return JsonResponse(responseDict)

def GetTranslatorAssignments(request):
    if request.method == 'GET':
        currentUser = auth.get_user(request).translator
        assignmentSet = currentUser.assignment_set.all()
        responseDict = {'assignmentList': []}
        for assignment in assignmentSet:
            task = assignment.task
            _task_tag = task.tag_set.all()
            _temp_tag_list = []
            for tag in _task_tag:
                _temp_tag_list.append(tag)
            responseDict['assignmentList'].append({
                'id': assignment.id,
                'status': assignment.status,
                'title': task.title,
                'publishTime': task.publishTime.timestamp(),
                'ddlTime': task.ddlTime.timestamp(),
                'tags': _temp_tag_list,
                'language': task.languageOrigin if task.languageOrigin == 0 else task.languageTarget,
                'description': assignment.description,
            })
        return JsonResponse(responseDict)

def PickupAssignment(request):
    if request.method == 'POST':
        user = auth.get_user(request).translator
        infoDict = json.loads(request.body.decode())
        taskId = infoDict['task_id']
        assignmentOrder = infoDict['assignment_order']
        task = Task.objects.get(id = taskId)
        assignment = Assignment.objects.get(task = task, order = assignmentOrder)
        with transaction.atomic():
            if assignment.status == 1:
                assignment.translator = user
                assignment.status = 2
                assignment.save()
            return JsonResponse({'translator': assignment.translator.username})
    
def GetTaskDetail(request):
    if request.method == 'GET':
        print('-----------------------GetTaskDetail-----------------')
        taskId = request.GET.get('taskid')
        task = Task.objects.get(id=taskId)

        responseDict = {
            'id': task.id,
            'title': task.title,
            'status': task.status,
            'description': task.description,
            'publishTime': task.publishTime.timestamp(),
            'ddlTime': task.ddlTime.timestamp(),
            'language': task.languageOrigin if task.languageOrigin == 0 else task.languageTarget,
            'fileUrl': task.fileUrl.name.split('/')[-1] if task.fileUrl else '',
            'employerId': task.employer.id,
            'assignment': []
        }
        assignment_set = task.assignment_set.all()
        for assignment in assignment_set:
            responseDict['assignment'].append({
                'id': assignment.id,
                'order': assignment.order,
                'description': assignment.description,
                'translator': assignment.translator.username if assignment.translator else '',
                'status': assignment.status,
                'score': assignment.scores,
                'price': assignment.price,
                'submission': assignment.submission.name.split('/')[-1] if assignment.submission else '',
            })
        return JsonResponse(responseDict)

def GetAssignmentDetail(request):
    if request.method == 'GET':
        print('-----------------------GetAssignmentDetail-----------------')
        assignmentId = request.GET.get('assignmentid')
        assignment = Assignment.objects.get(id=assignmentId)
        task = assignment.task
        responseDict = {
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
        return JsonResponse(responseDict)

def GetSquareTasks(request):
    if request.method == 'GET':
        print('-----------------------GetSquareTasks-----------------')
        # current_user = auth.get_user(request).employer
        taskSet = Task.objects.order_by('publishTime')
        if taskSet.count() > 5:
            taskSet = taskSet.reverse()[:5]
        responseDict = {'taskList': []}
        for task in taskSet:
            _task_tag = task.tag_set.all()
            _temp_tag_list = []
            for tag in _task_tag:
                _temp_tag_list.append(tag)

            assignmentSet = task.assignment_set.all()
            _temp_assignment = []
            for assignment in assignmentSet:
                _temp_assignment.append({
                    'order': assignment.order,
                    'description': assignment.description,
                    'translator': assignment.translator.username if assignment.translator else '',
                    'status': assignment.status,
                    'score': assignment.scores,
                    'price': assignment.price,
                    'submission': assignment.submission.url if assignment.submission else '',
                })

            responseDict['taskList'].append({
                'id': task.id,
                'title': task.title,
                'publishTime': task.publishTime.timestamp(),
                'ddlTime': task.ddlTime.timestamp(),
                'tags': _temp_tag_list,
                'language': task.languageOrigin if task.languageOrigin == 0 else task.languageTarget,
                'description': task.description,
                'assignment': _temp_assignment
            })
        return JsonResponse(responseDict)

def SubmitAssignment(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        assignmentId = request.POST.get('assignmentid')
        print(assignmentId)
        assignment = Assignment.objects.get(id = assignmentId)
        assignment.submission.save('assignments/' + file.name, file)
    return JsonResponse({'url': assignment.submission.name})

def PublishTask(request):
    if request.method == 'POST':
        infoDict = json.loads(request.body.decode())
        taskId = infoDict['taskid']
        task = Task.objects.get(id=taskId)
        task.status = 1
        task.save()
        assignmentSet = task.assignment_set.all()
        for assignment in assignmentSet:
            assignment.status = 1
            assignment.save()
        return JsonResponse({'status': True})


def SolveDispute(request):
    if request.method == 'POST':
        infoDict = json.loads(request.body.decode())
        disputeId = infoDict['disputeid']
        result = infoDict['result']
        statement = infoDict['statement']
        dispute = Dispute.objects.get(id=disputeId)
        dispute.adminStatement = statement
        if result:
            dispute.status = 1
        else:
            dispute.status = 2
        dispute.save()
        return JsonResponse({'status': True})

def VerifyLicense(request):
    if request.method == 'POST':
        infoDict = json.loads(request.body.decode())
        licenseId = infoDict['licenseid']
        result = infoDict['result']
        license = License.objects.get(id=licenseId)
        if result:
            license.adminVerify = 1
        else:
            license.adminVerify = 2
        license.save()
        return JsonResponse({'status': True})

def GetManager(request):
    if request.method == 'GET':
        print('-----------------------GetManager-----------------')
        responseDict = {
            'DisputeList': [],
            'LicenseList': []
        }
        disputeSet = Dispute.objects.filter(status=0)
        if disputeSet.count() > 100:
            disputeSet = disputeSet[:100]
        for dispute in disputeSet:
            responseDict['DisputeList'].append({
                'id': dispute.id,
                'assignment_name': dispute.assignment.description,
                'argument_translator': dispute.translatorStatement,
                'argument_employer': dispute.employerStatement,
            })
        licenseSet = License.objects.filter(adminVerify=0)
        if licenseSet.count() > 100:
            licenseSet = licenseSet[:100]
        for _license in licenseSet:
            responseDict['LicenseList'].append({
                'id': _license.id,
                'type': _license.licenseType,
                'url': _license.licenseImage.url,
            })
        return JsonResponse(responseDict)

def AcceptAssignment(request):
    if request.method == 'POST':
        infoDict = json.loads(request.body.decode())
        assignmentId = infoDict['assignmentid']
        result = infoDict['result']
        acceptance = infoDict['acceptance']
        assignment = Assignment.objects.get(id=assignmentId)
        if acceptance == 'accept':
            assignment.scores = result
        elif acceptance == 'reject':
            Dispute.objects.create(assignment=assignmentId, employerStatement=result)
        assignment.status = 3
        assignment.save()
        return JsonResponse({'status': True})

def FileDownload(request):
    def fileIterator(fileName, chunkSize=512):
        with open(fileName, 'rb') as f:
            while True:
                c = f.read(chunkSize)
                if c:
                    yield c
                else:
                    break
    if request.method == 'GET':
        downloadType = request.GET.get('type')
        root = 'C:/Users/yw/Desktop/Babel/media/' + downloadType
        filename = request.GET.get('filename')
        response = StreamingHttpResponse(fileIterator(root + '/' + filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
        return response

def UploadLicense(request):
    if request.method == 'POST':
        lfile = request.FILES.get('license')
        ltype = request.POST.get('type')
        if ltype == 'cet4':
            ltype = 4
        elif ltype == 'cet8':
            ltype = 8
        user = auth.get_user(request)
        _license = License.objects.create(licenseType = ltype, belonger = user.translator)
        _license.licenseImage.save('licenses/' + lfile.name, lfile)
    return JsonResponse({'url': user.avatar.name})