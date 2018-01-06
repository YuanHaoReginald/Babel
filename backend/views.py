from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import http
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
                         'avatar': '',
                         'level': user.creditLevel,
                         'experience': user.experience}
        if user.avatar:
            responseDict['avatar'] = user.avatar.url
        return JsonResponse(responseDict)


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
                         'language': '',
                         'avatar': user.avatar.url if user.avatar else ''}
        return JsonResponse(responseDict)

def UploadAvatar(request):
    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        user = auth.get_user(request)
        fileExtension = avatar.name.split('.')[-1]
        user.avatar.delete()
        user.avatar.save('avatars/' + user.username + '.' + fileExtension, avatar)
    return JsonResponse({'url': user.avatar.url})

def CreateTask(request):
    if request.method == 'POST':
        user = auth.get_user(request).employer
        infoDict = json.loads(request.body.decode())
        taskTitle = infoDict['title']
        taskDescription = infoDict['description']
        taskLanguage = infoDict['language']
        if infoDict['license'] == 'cet4':
            taskLicense = 4
        elif infoDict['license'] == 'cet8':
            taskLicense = 8
        taskLevel = infoDict['level']
        taskTags = infoDict['tags']
        taskDdlTime = infoDict['ddlTime']
        taskAssignments = infoDict['assignments']
        if infoDict['language'] == 'English':
            taskLanguageTarget = 1
        elif infoDict['language'] == 'Japanese':
            taskLanguageTarget = 2
        elif infoDict['language'] == 'French':
            taskLanguageTarget = 5
        elif infoDict['language'] == 'Russian':
            taskLanguageTarget = 4
        elif infoDict['language'] == 'Spanish':
            taskLanguageTarget = 5
        if infoDict['if_test'] == '需要':
            taskTestText = infoDict['testText']
        else:
            taskTestText = ''
        task = Task.objects.create(title = taskTitle,
                                   description = taskDescription,
                                   fileType = 0,
                                   employer = user,
                                   ddlTime = datetime.datetime.utcfromtimestamp(taskDdlTime),
                                   languageTarget = taskLanguageTarget,
                                   requirementCreditLevel = taskLevel,
                                   requirementLicense = taskLicense,
                                   testText = taskTestText)
        for tag in taskTags:
            Tag.objects.get(tag=tag).tasks.add(task)
        for assignment in taskAssignments:
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
                _temp_tag_list.append(tag.tag)
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
                _temp_tag_list.append(tag.tag)
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
        # Check Translator Qualification Review
        if user.creditLevel < task.requirementCreditLevel:
            return JsonResponse({'status': False, 'reason': 'Level don\'t meet requirements.'})
        licenseSet = user.license_set.filter(adminVerify=1)
        flag = False
        for _license in licenseSet:
            if _license.licenseType // 10 == task.languageTarget:
                flag = True
                break
        if not flag:
            return JsonResponse({'status': False, 'reason': 'Language License don\'t meet requirements.'})
        # Try Receive Assignment
        with transaction.atomic():
            if assignment.status == 1:
                assignment.translator = user
                assignment.status = 2
                assignment.save()
                return JsonResponse({'status': True})
            else:
                return JsonResponse({'status': False, 'reason': 'Assignment has been picked up by others.'})
    
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
            'language': task.languageTarget if task.languageOrigin == 0 else task.languageTarget,
            'fileUrl': task.fileUrl.name.split('/')[-1] if task.fileUrl else '',
            'employerId': task.employer.id,
            'requirementLevel': task.requirementCreditLevel,
            'requirementLicense': task.requirementLicense,
            'testText': task.testText,
            'assignment': []
        }
        assignment_set = task.assignment_set.all()
        for assignment in assignment_set:
            _dispute = Dispute.objects.filter(assignment=assignment)
            statement = ''
            if len(_dispute) != 0 and _dispute[0].adminStatement:
                statement = _dispute[0].adminStatement
            responseDict['assignment'].append({
                'id': assignment.id,
                'hasDispute' : len(_dispute) != 0,
                'disputeResult' : _dispute[0].status if len(_dispute) != 0 else 0,
                'statement' : statement,
                'order': assignment.order,
                'description': assignment.description,
                'translator': assignment.translator.username if assignment.translator else '',
                'status': assignment.status,
                'score': assignment.scores,
                'price': assignment.price,
                'testResult': assignment.testResult,
                'submission': assignment.submission.name.split('/')[-1] if assignment.submission else '',
            })
        return JsonResponse(responseDict)

def GetAssignmentDetail(request):
    if request.method == 'GET':
        print('-----------------------GetAssignmentDetail-----------------')
        assignmentid = request.GET.get('assignmentid')
        assignment = Assignment.objects.get(id=assignmentid)
        _dispute = Dispute.objects.filter(assignment=assignment)
        statement = ''
        if len(_dispute) != 0 and _dispute[0].adminStatement:
            statement = _dispute[0].adminStatement
        task = assignment.task
        responseDict = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'publishTime': task.publishTime.timestamp(),
            'ddlTime': task.ddlTime.timestamp(),
            'language': task.languageOrigin if task.languageOrigin == 0 else task.languageTarget,
            'assignment': {
                'id': assignment.id,
                'hasDispute' : len(_dispute) != 0,
                'disputeResult' : _dispute[0].status if len(_dispute) != 0 else 0,
                'statement' : statement,
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
        keyword = request.GET.get('keyword')
        taskSet = Task.objects.filter(status=1).order_by('publishTime')
        if keyword != None:
            taskSet = taskSet.filter(title__contains = keyword)
        if taskSet.count() > 50:
            taskSet = taskSet.reverse()[:50]
        responseDict = {'taskList': []}
        for task in taskSet:
            _task_tag = task.tag_set.all()
            _temp_tag_list = []
            for tag in _task_tag:
                _temp_tag_list.append(tag.tag)

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
                'language': task.languageTarget if task.languageOrigin == 0 else task.languageTarget,
                'description': task.description,
                'testText': task.testText,
                'assignment': _temp_assignment
            })
        return JsonResponse(responseDict)

def SubmitAssignment(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        assignmentId = request.POST.get('assignmentid')
        assignment = Assignment.objects.get(id = assignmentId)
        assignment.submission.save('assignments/' + file.name, file)
    return JsonResponse({'url': assignment.submission.name.split('/')[-1]})

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
        dispute.assignment.status = 3
        dispute.assignment.save()
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
            assignment.status = 3            
        elif acceptance == 'reject':
            assignment.comment = result
            assignment.status = 4
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
        response = http.StreamingHttpResponse(fileIterator(root + '/' + filename))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
        return response

def UploadLicense(request):
    if request.method == 'POST':
        lfile = request.FILES.get('license')
        ltype = request.POST.get('type')
        language = request.POST.get('language')

        if ltype == 'cet4':
            ltype = 4
        elif ltype == 'cet8':
            ltype = 8
        else:
            pass


        if language == 'English':
            ltype += 10
        elif language == 'Japanese':
            ltype += 20
        elif language == 'French':
            ltype += 30
        elif language == 'Russian':
            ltype += 40
        elif language == 'Spanish':
            ltype += 50
        else:
            pass

        user = auth.get_user(request)
        _license = License.objects.create(licenseType = ltype, belonger = user.translator)
        _license.licenseImage.save('licenses/' + lfile.name, lfile)
    return JsonResponse({'url': _license.name.split('/')[-1]})

def ResponseTestResult(request):
    if request.method == 'POST':
        infoDict = json.loads(request.body.decode())
        assignmentId  = infoDict['assignment_id']
        assignment = Assignment.objects.get(id = assignmentId)
        result = infoDict['result']
        if result:
            assignment.status = 2
        else:
            assignment.status = 1
            assignment.translator = None
        assignment.save()
        return HttpResponse(0)

def SubmitTestResult(request):
    if request.method == 'POST':
        user = auth.get_user(request).translator
        infoDict = json.loads(request.body.decode())
        taskId = infoDict['task_id']
        assignmentOrder = infoDict['assignment_order']
        testResult = infoDict['testResult']
        task = Task.objects.get(id = taskId)
        assignment = Assignment.objects.get(task = task, order = assignmentOrder)
        with transaction.atomic():
            if assignment.status == 1:
                assignment.translator = user
                assignment.status = 10
                assignment.testResult = testResult
                assignment.save()
            return JsonResponse({'translator': assignment.translator.username})

def AcceptResult(request):
    if request.method == 'POST':
        infoDict = json.loads(request.body.decode())
        assignment = Assignment.objects.get(id=infoDict['assignmentId'])
        assignment.status = 3
        assignment.save()
        return JsonResponse({'status': True})

def ArgueResult(request):
    if request.method == 'POST':
        infoDict = json.loads(request.body.decode())
        assignment = Assignment.objects.get(id=infoDict['assignmentId'])
        Dispute.objects.create(assignment=assignment, employerStatement=assignment.comment, translatorStatement=infoDict['text'])
        return JsonResponse({'status': True})
