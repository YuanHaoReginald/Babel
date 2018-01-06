from django.test import TestCase
from django.test.client import Client
from .views import *
from .models import *
from django.core.urlresolvers import resolve
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from unittest.mock import Mock,patch,MagicMock
from django.http import HttpRequest
import backend.urls
import json

# Create your tests here.
class UserSignUpTestCase(TestCase):
    def test_employer_sign_up_with_normal_username(self):
        found = resolve('/UserSignUp', urlconf = backend.urls)
        request = Mock(wraps= HttpRequest() , method = 'POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"shaoyushan1996","password":"123456","email":"123@163.com","utype":"employer"}')
        with patch.object(auth, 'login', return_value=Mock(student_id=1)) as MockUser:
            response = json.loads(found.func(request).content.decode())
            self.assertNotEqual(response['id'], 0)

    def test_translator_sign_up_with_normal_username(self):
        found = resolve('/UserSignUp', urlconf = backend.urls)
        request = Mock(wraps= HttpRequest() , method = 'POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"shaoyushan1996","password":"123456","email":"123@163.com","utype":"translator"}')
        with patch.object(auth, 'login', return_value=Mock(student_id=1)) as MockUser:
            response = json.loads(found.func(request).content.decode())
            self.assertNotEqual(response['id'], 0)

    def test_employer_sign_up_with_repeated_username(self):
        found = resolve('/UserSignUp', urlconf = backend.urls)
        request = Mock(wraps= HttpRequest() , method = 'POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"shaoyushan1996","password":"123456","email":"123@163.com","utype":"employer"}')
        with patch.object(auth, 'login', return_value=Mock(student_id=1)) as MockUser:
            response = json.loads(found.func(request).content.decode())

        request1 = Mock(wraps=HttpRequest(), method='POST')
        request1.body = Mock()
        request1.body.decode = Mock(
            return_value='{"username":"shaoyushan1996","password":"1234567","email":"321@163.com","utype":"employer"}')
        with patch.object(auth, 'login', return_value=Mock(student_id=1)) as MockUser:
            response1 = json.loads(found.func(request1).content.decode())
            self.assertEqual(response1['id'], 0)

class UserSignInTestCase(TestCase):
    def test_user_exist(self):
        found = resolve('/UserSignUp', urlconf = backend.urls)
        request = Mock(wraps= HttpRequest() , method = 'POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"shaoyushan1996","password":"123456","email":"123@163.com","utype":"employer"}')
        with patch.object(auth, 'login', return_value=Mock(student_id=1)) as MockUser:
            response = json.loads(found.func(request).content.decode())

        found1 = resolve('/UserSignIn', urlconf=backend.urls)
        request1 = Mock(wraps=HttpRequest(), method='POST')
        request1.body = Mock()
        request1.body.decode = Mock(
            return_value='{"username":"shaoyushan1996","password":"123456","utype":"employer"}')
        with patch.object(auth, 'authenticate', return_value=Mock(id = 1,utype = 'employer')) as MockUser:
            with patch.object(auth, 'login', return_value=Mock(student_id=1)) as MockUser:
                response1 = json.loads(found1.func(request1).content.decode())
                self.assertNotEqual(response1['id'], 0)

    def test_user_not_exist(self):
        found1 = resolve('/UserSignIn', urlconf=backend.urls)
        request1 = Mock(wraps=HttpRequest(), method='POST')
        request1.body = Mock()
        request1.body.decode = Mock(
            return_value='{"username":"shaoyushan1996","password":"123456","utype":"employer"}')
        with patch.object(auth, 'authenticate', return_value = None ) as MockUser:
            response1 = json.loads(found1.func(request1).content.decode())
            self.assertEqual(response1['id'], 0)

class UsernameCheckTestCase(TestCase):
    def test_normal_test_case(self):
        found = resolve('/UsernameCheck', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')
        request.body = Mock()
        request.body.decode = Mock(
            return_value='{"username":"shaoyushan1996","password":"123456","email":"123@163.com","utype":"employer"}')

        with patch.object(User.objects, 'get', return_value=Mock(student_id=1)) as MockUser:
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['status'], True)

class UserLogoutTestCase(TestCase):
    def test_common_user_log_out(self):
        found = resolve('/UserLogout', urlconf = backend.urls)
        request = Mock(wraps= HttpRequest() , method = 'POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"shaoyushan1996","password":"123456","email":"123@163.com","utype":"employer"}')
        with patch.object(auth, 'logout', return_value=Mock()) as MockUser:
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response, 0)

class GetUserInfoTestCase(TestCase):
    def test_get_translator_info(self):
        found = resolve('/GetUserInfo', urlconf = backend.urls)
        myavatar = Mock(url = '123.jpg')
        request = Mock(wraps= HttpRequest() , method = 'GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"shaoyushan1996","password":"123456","email":"123@163.com","utype":"translator"}')
        with patch.object(auth, 'get_user', return_value=Mock(username = 'shaoyushan',email = '123@163.com',
                                                              headSrc = '', creditLevel = 2, experience = 2,avatar = myavatar
                                                              )) as MockUser:
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['username'], 'shaoyushan')

    def test_get_employer_info(self):
        found = resolve('/GetUserInfo', urlconf = backend.urls)
        myavatar = Mock(url = '123.jpg')
        request = Mock(wraps= HttpRequest() , method = 'GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"username":"shaoyushan1996","password":"123456","email":"123@163.com","utype":"employer"}')
        with patch.object(auth, 'get_user', return_value=Mock(username = 'shaoyushan',email = '123@163.com',
                                                              headSrc = '', creditLevel = 2, experience = 2,avatar = myavatar
                                                              )) as MockUser:
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['username'], 'shaoyushan')

class UserModifyTestCase(TestCase):
    def test_translator_post(self):

        myavatar = Mock(url='123.jpg')
        user_translator = Mock(telephone = '13333333333',alipayNumber = 'ali',wechatNumber = 'wechat',avatar = myavatar)
        found = resolve('/UserModify', urlconf = backend.urls)
        request = Mock(wraps = HttpRequest(), method = 'POST')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"telephone":"13333333333","alipayNumber":"alipay","wechatNumber":"wechat","utype":"translator"}')
        with patch.object(auth, 'get_user', return_value=Mock(translator = user_translator,utype = 'translator')) as MockUser:
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['status'], True)

    def test_employer_GET(self):

        found = resolve('/UserModify', urlconf = backend.urls)
        myavatar = Mock(url='123.jpg')
        user_employer = Mock(telephone = '13333333333',alipayNumber = 'ali',wechatNumber = 'wechat',avatar = myavatar,utype = 'employer')
        request = Mock(wraps = HttpRequest(), method = 'GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"telephone":"13333333333","alipayNumber":"alipay","wechatNumber":"wechat","utype":"employer"}')
        with patch.object(auth, 'get_user', return_value=Mock(employer = user_employer, utype = 'employer')) as MockUser:
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['telephone'], '13333333333')

# not finish
class UploadAvatarTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/UploadAvatar', urlconf = backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        myavatar = Mock()
        myavatar.name = 'a.jpg'
        myavatar.url = 'a.jpg'
        myuser = Mock()
        myuser.username = 'shaoyushan'
        myuser.avatar = myavatar

        with patch.object(request.FILES,'get',return_value = myavatar):
            with patch.object(auth, 'get_user', return_value = myuser) as MockUser:
                response = json.loads(found.func(request).content.decode())
                self.assertEqual(response['url'], 'a.jpg')


class CreateTaskTestCase(TestCase):
    def test_normal_test_English(self):
        found = resolve('/CreateTask', urlconf = backend.urls)
        request = Mock(wraps= HttpRequest() , method = 'POST')
        mytask = Mock()
        mytask.add = lambda x : True
        request.body = Mock()
        request.body.decode = Mock(return_value = ' {"tags":[1,2,3],"if_test":"需要","testText":"a small text","title":"a title","description":"a des","language":"English","license":"cet4","level":2.1,"tags":"123","ddlTime":123456.23,"assignments":[{"price":123,"order":123,"text":"asd"}] }')
        with patch.object(auth, 'get_user', return_value = Mock(employer = Mock(creditLevel = 1.1,
                                                                                experience = 1,
                                                                                telephone = '123',
                                                                                alipayNumber = 'ali',
                                                                                wechatNumber = 'wechat'
                                                              ))) as MockUser:
            with patch.object(Task.objects,'create', return_value = Mock(id = 1, title = '123', description = '456', fileType = 0, employer = Mock(creditLevel = 1.1,
                                                                                experience = 1,
                                                                                telephone = '123',
                                                                                alipayNumber = 'ali',
                                                                                wechatNumber = 'wechat'), ddlTime = 123.4, languageTarget = 3, requirementCreditLevel = 2.2 )):
                with patch.object(Assignment.objects,'create', return_value = Mock(task = None, order = 1,description = '1243')):
                    with patch.object(Tag.objects,"get",return_value = mytask):
                        response = json.loads(found.func(request).content.decode())
                        self.assertEqual(response['task_id'], 1)

    def test_normal_test_Japanese(self):
        found = resolve('/CreateTask', urlconf = backend.urls)
        request = Mock(wraps= HttpRequest() , method = 'POST')
        mytask = Mock()
        mytask.add = lambda x : True
        request.body = Mock()
        request.body.decode = Mock(return_value = ' {"tags":[1,2,3],"if_test":"需要","testText":"a small text","title":"a title","description":"a des","language":"Japanese","license":"cet4","level":2.1,"tags":"123","ddlTime":123456.23,"assignments":[{"price":123,"order":123,"text":"asd"}] }')
        with patch.object(auth, 'get_user', return_value = Mock(employer = Mock(creditLevel = 1.1,
                                                                                experience = 1,
                                                                                telephone = '123',
                                                                                alipayNumber = 'ali',
                                                                                wechatNumber = 'wechat'
                                                              ))) as MockUser:
            with patch.object(Task.objects,'create', return_value = Mock(id = 1, title = '123', description = '456', fileType = 0, employer = Mock(creditLevel = 1.1,
                                                                                experience = 1,
                                                                                telephone = '123',
                                                                                alipayNumber = 'ali',
                                                                                wechatNumber = 'wechat'), ddlTime = 123.4, languageTarget = 3, requirementCreditLevel = 2.2 )):
                with patch.object(Assignment.objects,'create', return_value = Mock(task = None, order = 1,description = '1243')):
                    with patch.object(Tag.objects,"get",return_value = mytask):
                        response = json.loads(found.func(request).content.decode())
                        self.assertEqual(response['task_id'], 1)

    def test_normal_test_French(self):
        found = resolve('/CreateTask', urlconf = backend.urls)
        request = Mock(wraps= HttpRequest() , method = 'POST')
        mytask = Mock()
        mytask.add = lambda x : True
        request.body = Mock()
        request.body.decode = Mock(return_value = ' {"tags":[1,2,3],"if_test":"需要","testText":"a small text","title":"a title","description":"a des","language":"French","license":"cet4","level":2.1,"tags":"123","ddlTime":123456.23,"assignments":[{"price":123,"order":123,"text":"asd"}] }')
        with patch.object(auth, 'get_user', return_value = Mock(employer = Mock(creditLevel = 1.1,
                                                                                experience = 1,
                                                                                telephone = '123',
                                                                                alipayNumber = 'ali',
                                                                                wechatNumber = 'wechat'
                                                              ))) as MockUser:
            with patch.object(Task.objects,'create', return_value = Mock(id = 1, title = '123', description = '456', fileType = 0, employer = Mock(creditLevel = 1.1,
                                                                                experience = 1,
                                                                                telephone = '123',
                                                                                alipayNumber = 'ali',
                                                                                wechatNumber = 'wechat'), ddlTime = 123.4, languageTarget = 3, requirementCreditLevel = 2.2 )):
                with patch.object(Assignment.objects,'create', return_value = Mock(task = None, order = 1,description = '1243')):
                    with patch.object(Tag.objects,"get",return_value = mytask):
                        response = json.loads(found.func(request).content.decode())
                        self.assertEqual(response['task_id'], 1)

    def test_normal_test_Russian(self):
        found = resolve('/CreateTask', urlconf = backend.urls)
        request = Mock(wraps= HttpRequest() , method = 'POST')
        mytask = Mock()
        mytask.add = lambda x : True
        request.body = Mock()
        request.body.decode = Mock(return_value = ' {"tags":[1,2,3],"if_test":"需要","testText":"a small text","title":"a title","description":"a des","language":"Russian","license":"cet4","level":2.1,"tags":"123","ddlTime":123456.23,"assignments":[{"price":123,"order":123,"text":"asd"}] }')
        with patch.object(auth, 'get_user', return_value = Mock(employer = Mock(creditLevel = 1.1,
                                                                                experience = 1,
                                                                                telephone = '123',
                                                                                alipayNumber = 'ali',
                                                                                wechatNumber = 'wechat'
                                                              ))) as MockUser:
            with patch.object(Task.objects,'create', return_value = Mock(id = 1, title = '123', description = '456', fileType = 0, employer = Mock(creditLevel = 1.1,
                                                                                experience = 1,
                                                                                telephone = '123',
                                                                                alipayNumber = 'ali',
                                                                                wechatNumber = 'wechat'), ddlTime = 123.4, languageTarget = 3, requirementCreditLevel = 2.2 )):
                with patch.object(Assignment.objects,'create', return_value = Mock(task = None, order = 1,description = '1243')):
                    with patch.object(Tag.objects,"get",return_value = mytask):
                        response = json.loads(found.func(request).content.decode())
                        self.assertEqual(response['task_id'], 1)

    def test_normal_test_Spanish(self):
        found = resolve('/CreateTask', urlconf = backend.urls)
        request = Mock(wraps= HttpRequest() , method = 'POST')
        mytask = Mock()
        mytask.add = lambda x : True
        request.body = Mock()
        request.body.decode = Mock(return_value = ' {"tags":[1,2,3],"if_test":"需要","testText":"a small text","title":"a title","description":"a des","language":"Spanish","license":"cet4","level":2.1,"tags":"123","ddlTime":123456.23,"assignments":[{"price":123,"order":123,"text":"asd"}] }')
        with patch.object(auth, 'get_user', return_value = Mock(employer = Mock(creditLevel = 1.1,
                                                                                experience = 1,
                                                                                telephone = '123',
                                                                                alipayNumber = 'ali',
                                                                                wechatNumber = 'wechat'
                                                              ))) as MockUser:
            with patch.object(Task.objects,'create', return_value = Mock(id = 1, title = '123', description = '456', fileType = 0, employer = Mock(creditLevel = 1.1,
                                                                                experience = 1,
                                                                                telephone = '123',
                                                                                alipayNumber = 'ali',
                                                                                wechatNumber = 'wechat'), ddlTime = 123.4, languageTarget = 3, requirementCreditLevel = 2.2 )):
                with patch.object(Assignment.objects,'create', return_value = Mock(task = None, order = 1,description = '1243')):
                    with patch.object(Tag.objects,"get",return_value = mytask):
                        response = json.loads(found.func(request).content.decode())
                        self.assertEqual(response['task_id'], 1)


class UploadTaskFileTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/UploadTaskFile', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        myfile = Mock()
        myfile.name = 'abc.doc'
        mytask = Mock()
        mytask.fileUrl.name = 'abc.doc'

        with patch.object(request.FILES,'get',return_value = myfile ):
            with patch.object(request.POST,'get',return_value = 1):
                with patch.object(Task.objects,'get',return_value = mytask ):
                    response = json.loads(found.func(request).content.decode())
                    self.assertEqual(response['url'], 'abc.doc')


class GetEmployerTasksTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/GetEmployerTasks', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='GET')

        myTag = Mock()
        myTag.tag = 1

        myTaskTag = [myTag]

        myTask = Mock()
        myTask.tag_set.all = lambda : myTaskTag
        myTask.id = 1
        myTask.title = "test title"
        myTask.status = 1
        myTask.publishTime.timestamp = lambda : 112
        myTask.ddlTime.timestamp = lambda : 114
        myTask.languageOrigin = 1
        myTask.languageTarget = 2
        myTask.description = '123'


        myCurrentUser = Mock()
        myCurrentUser.task_set.all = lambda : [myTask]

        myUser = Mock()
        myUser.employer = myCurrentUser

        with patch.object(auth,"get_user",return_value = myUser):
            response = json.loads(found.func(request).content.decode())
            test_task =  response['taskList'][0]
            self.assertEqual(test_task['id'], 1)

class GetTranslatorAssignmentsTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/GetTranslatorAssignments', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='GET')

        myTag = Mock()
        myTag.tag = 1

        myTask = Mock()
        myTask.tag_set.all = lambda : [myTag]
        myTask.id = 1
        myTask.title = "test title"
        myTask.status = 1
        myTask.publishTime.timestamp = lambda : 112
        myTask.ddlTime.timestamp = lambda : 114
        myTask.languageOrigin = 1
        myTask.languageTarget = 2
        myTask.description = '123'

        myAssignment = Mock()
        myAssignment.task = myTask
        myAssignment.id = 1
        myAssignment.status = 1
        myAssignment.description = '123'

        myCurrentUser = Mock()
        myCurrentUser.assignment_set.all = lambda : [myAssignment]

        myUser = Mock()
        myUser.translator = myCurrentUser

        with patch.object(auth,"get_user",return_value = myUser):
            response = json.loads(found.func(request).content.decode())
            test_task =  response['assignmentList'][0]
            self.assertEqual(test_task['id'], 1)

class PickupAssignmentTestCase(TestCase):
    def test_normal_test_one(self):
        found = resolve('/PickupAssignment', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        request.body = Mock()
        request.body.decode = Mock(return_value='{"task_id":1,"assignment_order":1}')

        myUser = Mock()
        myCurrentUser = Mock()
        myCurrentUser.translator = myUser
        myUser.creditLevel = 1

        myTask = Mock()
        myTask.requirementCreditLevel = 2
        myTask.languageTarget = 1

        myAssignment = Mock()
        myAssignment.status = 1

        with patch.object(auth,'get_user',return_value = myCurrentUser):
            with patch.object(Task.objects,'get',return_value = myTask):
                with patch.object(Assignment.objects,'get',return_value = myAssignment):
                    response = json.loads(found.func(request).content.decode())
                    self.assertEqual(response['status'], False)

    def test_normal_test_two(self):
        found = resolve('/PickupAssignment', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        request.body = Mock()
        request.body.decode = Mock(return_value='{"task_id":1,"assignment_order":1}')

        myUser = Mock()
        myCurrentUser = Mock()
        myCurrentUser.translator = myUser
        myUser.creditLevel = 3
        myLicense = Mock()
        myLicense.licenseType = 4
        myUser.license_set.filter = lambda adminVerify : [myLicense]

        myTask = Mock()
        myTask.requirementCreditLevel = 2
        myTask.languageTarget = 1

        myAssignment = Mock()
        myAssignment.status = 1

        with patch.object(auth,'get_user',return_value = myCurrentUser):
            with patch.object(Task.objects,'get',return_value = myTask):
                with patch.object(Assignment.objects,'get',return_value = myAssignment):
                    response = json.loads(found.func(request).content.decode())
                    self.assertEqual(response['status'], False)

    def test_normal_test_three(self):
        found = resolve('/PickupAssignment', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        request.body = Mock()
        request.body.decode = Mock(return_value='{"task_id":1,"assignment_order":1}')

        myUser = Mock()
        myCurrentUser = Mock()
        myCurrentUser.translator = myUser
        myUser.creditLevel = 3
        myLicense = Mock()
        myLicense.licenseType = 10
        myUser.license_set.filter = lambda adminVerify: [myLicense]

        myTask = Mock()
        myTask.requirementCreditLevel = 2
        myTask.languageTarget = 1

        myAssignment = Mock()
        myAssignment.status = 1

        with patch.object(auth, 'get_user', return_value=myCurrentUser):
            with patch.object(Task.objects, 'get', return_value=myTask):
                with patch.object(Assignment.objects, 'get', return_value=myAssignment):
                    response = json.loads(found.func(request).content.decode())
                    self.assertEqual(response['status'], True)

    def test_normal_test_four(self):
        found = resolve('/PickupAssignment', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        request.body = Mock()
        request.body.decode = Mock(return_value='{"task_id":1,"assignment_order":1}')

        myUser = Mock()
        myCurrentUser = Mock()
        myCurrentUser.translator = myUser
        myUser.creditLevel = 3
        myLicense = Mock()
        myLicense.licenseType = 10
        myUser.license_set.filter = lambda adminVerify: [myLicense]

        myTask = Mock()
        myTask.requirementCreditLevel = 2
        myTask.languageTarget = 1

        myAssignment = Mock()
        myAssignment.status = 2

        with patch.object(auth, 'get_user', return_value=myCurrentUser):
            with patch.object(Task.objects, 'get', return_value=myTask):
                with patch.object(Assignment.objects, 'get', return_value=myAssignment):
                    response = json.loads(found.func(request).content.decode())
                    self.assertEqual(response['status'], False)

class GetTaskDetailTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/GetTaskDetail', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='GET')

        myTask = Mock()
        myTask.id = 1
        myTask.title = 'title'
        myTask.status = 1
        myTask.description = '123'
        myTask.publishTime.timestamp = lambda : 1234
        myTask.ddlTime.timestamp = lambda :567
        myTask.languageTarget = 1
        myTask.languageOrigin = 2
        myTask.fileUrl.name = 'a/jpg'
        myTask.employer.id = 1
        myTask.testText = '1234'
        myTask.requirementCreditLevel = 1
        myTask.requirementLicense = 'CET4'

        myAssignment = Mock()
        myAssignment.id = 1
        myAssignment.order = 1
        myAssignment.description = '12345'
        myAssignment.translator.username = 'shao'
        myAssignment.status = 1
        myAssignment.scores = 1
        myAssignment.price = 123
        myAssignment.testResult = 'test'
        myAssignment.submission.name = '12/34/56'

        myTask.assignment_set.all = lambda : [myAssignment]

        aDispute = Mock()
        aDispute.adminStatement = '123456'
        aDispute.status = 1
        myDispute = [aDispute]

        with patch.object(request.GET,'get',return_value = 1):
            with patch.object(Task.objects,'get',return_value = myTask):
                with patch.object(Dispute.objects,'filter',return_value = myDispute):
                    response = json.loads(found.func(request).content.decode())
                    test_task = response['assignment'][0]
                    self.assertEqual(test_task['id'], 1)

class GetAssignmentDetailTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/GetAssignmentDetail', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='GET')

        aDispute = Mock()
        aDispute.adminStatement = '123456'
        aDispute.status = 1
        myDispute = [aDispute]

        myTask = Mock()
        myTask.id = 1
        myTask.title = 'title'
        myTask.status = 1
        myTask.description = '123'
        myTask.publishTime.timestamp = lambda : 1234
        myTask.ddlTime.timestamp = lambda :567
        myTask.languageTarget = 1
        myTask.languageOrigin = 2
        myTask.fileUrl.name = 'a/jpg'
        myTask.employer.id = 1
        myTask.testText = '1234'
        myTask.employer.username = 'abc'
        myTask.employer.avatar.url = 'hhh'

        myAssignment = Mock()
        myAssignment.id = 1
        myAssignment.order = 1
        myAssignment.description = '12345'
        myAssignment.translator.username = 'shao'
        myAssignment.status = 1
        myAssignment.scores = 1
        myAssignment.price = 123
        myAssignment.testResult = 'test'
        myAssignment.submission.name = '12/34/56'
        myAssignment.task = myTask

        with patch.object(request.GET,'get',return_value = 1):
            with patch.object(Assignment.objects,'get',return_value = myAssignment):
                with patch.object(Dispute.objects,'filter',return_value = myDispute):
                    response = json.loads(found.func(request).content.decode())
                    test_task = response['assignment']
                    self.assertEqual(test_task['id'], 1)

# a problem...
class GetSquareTasksTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/GetSquareTasks', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='GET')

        myTag = Mock()
        myTag.tag = 1

        myAssignment = Mock()
        myAssignment.id = 1
        myAssignment.order = 1
        myAssignment.description = '12345'
        myAssignment.translator.username = 'shao'
        myAssignment.status = 1
        myAssignment.scores = 1
        myAssignment.price = 123
        myAssignment.testResult = 'test'
        myAssignment.submission.url = '12/34/56'

        myTask = Mock()
        myTask.id = 1
        myTask.title = 'title'
        myTask.status = 1
        myTask.description = '123'
        myTask.publishTime.timestamp = lambda : 1234
        myTask.ddlTime.timestamp = lambda :567
        myTask.languageTarget = 1
        myTask.languageOrigin = 2
        myTask.fileUrl.name = 'a/jpg'
        myTask.employer.id = 1
        myTask.testText = '1234'
        myTask.employer.username = 'abc'
        myTask.employer.avatar.url = 'hhh'
        myTask.tag_set.all = lambda : [myTag]
        myTask.assignment_set.all = lambda : [myAssignment]

        myTaskSet = MagicMock()
        myTaskSet.__iter__.return_value = [myTask]
        myTaskSet.count = lambda : 5

        taskSetUnorder = Mock()
        taskSetUnorder.order_by = lambda str : myTaskSet

        with patch.object(request.GET,'get', return_value = None):
            with patch.object(Task.objects,'filter',return_value = taskSetUnorder):
                #with patch.object(myTaskSet,'count'):
                    response = json.loads(found.func(request).content.decode())
                    test_task = response['taskList'][0]
                    self.assertEqual(test_task['id'], 1)


class SubmitAssignmentTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/SubmitAssignment', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        myfile = Mock()
        myfile.name = 'abc.doc'
        myassignment = Mock()
        myassignment.submission.name = 'abc.doc'

        with patch.object(request.FILES,'get',return_value = myfile):
            with patch.object(request.POST,'get',return_value = 1):
                with patch.object(Assignment.objects,'get',return_value = myassignment):
                    response = json.loads(found.func(request).content.decode())
                    self.assertEqual(response['url'], 'abc.doc')

class PublishTaskTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/PublishTask', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        request.body = Mock()
        request.body.decode = Mock(return_value=' {"taskid":1}')

        myass = Mock()
        myass.status = 1
        mytask = Mock()
        mytask.status = 1
        mytask.assignment_set.all = lambda :[myass]

        with patch.object(Task.objects,'get',return_value = mytask):
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['status'], True)

class SolveDisputeTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/SolveDispute', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        request.body = Mock()
        request.body.decode = Mock(return_value=' {"disputeid":1,"result":123,"statement":"haha"}')

        mydispute = Mock()
        mydispute.adminStatement = None
        mydispute.status = 0

        with patch.object(Dispute.objects,'get',return_value = mydispute):
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['status'], True)

class VerifyLicenseTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/VerifyLicense', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        request.body = Mock()
        request.body.decode = Mock(return_value=' {"licenseid":1,"result":123,"statement":"haha"}')

        mylicense = Mock()
        mylicense.adminVerify = 0

        with patch.object(License.objects,'get',return_value = mylicense):
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['status'], True)

class GetManagerTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/GetManager', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='GET')

        myDispute = Mock()
        myDispute.id = 1
        myDispute.assignment.description = 'assignment name'
        myDispute.translatorStatement = 'statement'
        myDispute.employerStatement = 'statement'
        myDisputeSet = MagicMock()
        myDisputeSet.count = lambda : 5
        myDisputeSet.__iter__.return_value = [myDispute]

        myLicense = Mock()
        myLicense.id = 1
        myLicense.licenseType = 'CET4'
        myLicense.licenseImage.url = 'a.jpg'
        myLicenseSet = MagicMock()
        myLicenseSet.count = lambda :5
        myLicenseSet.__iter__.return_value = [myLicense]

        with patch.object(Dispute.objects,'filter',return_value = myDisputeSet):
            with patch.object(License.objects,'filter',return_value = myLicenseSet):
                response = json.loads(found.func(request).content.decode())
                #test_license = response['licenseList'][0]
                test_dispute = response['DisputeList'][0]
                self.assertEqual(test_dispute['id'], 1)

class AcceptAssignmentTestCase(TestCase):
    def test_case_accept(self):
        found = resolve('/AcceptAssignment', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        request.body = Mock()
        request.body.decode = Mock(return_value=' {"assignmentid":1,"result":123,"acceptance":"accept"}')

        myAssignment = Mock()
        myAssignment.scores = 1
        myAssignment.status = 1
        myAssignment.comment = '123'

        with patch.object(Assignment.objects,'get',return_value = myAssignment):
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['status'], True)

    def test_case_reject(self):
        found = resolve('/AcceptAssignment', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        request.body = Mock()
        request.body.decode = Mock(return_value=' {"assignmentid":1,"result":123,"acceptance":"reject"}')

        myAssignment = Mock()
        myAssignment.scores = 1
        myAssignment.status = 1
        myAssignment.comment = '123'

        with patch.object(Assignment.objects,'get',return_value = myAssignment):
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['status'], True)

class FileDownloadTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/FileDownload', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='GET')

        filenameAndType = 'all.jpg'
        myres = {'Content-Type':'application/octet-stream','Content-Disposition':'attachment;filename="{0}"'}

        with patch.object(request.GET,'get',return_value = filenameAndType):
            with patch.object(http,'StreamingHttpResponse',return_value = myres):
                response = found.func(request)
                self.assertEqual(response['Content-Type'], 'application/octet-stream')

class UploadLicenseTestCase(TestCase):
    def test_cet4(self):
        found = resolve('/UploadLicense', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        myUser = Mock()
        myUser.translator = None

        mylfile = Mock()
        mylfile.name = 'a.jpg'

        myLicense = Mock()
        myLicense.name = 'a/b'

        with patch.object(auth,'get_user',return_value = myUser):
            with patch.object(request.FILES,'get',return_value = mylfile):
                with patch.object(request.POST,'get',return_value = 'cet4'):
                    with patch.object(myLicense.licenseImage,'save',return_value = 1):
                        with patch.object(License.objects,'create',return_value= myLicense):
                            response = json.loads(found.func(request).content.decode())
                            self.assertEqual(response['url'], "b")

    def test_cet8(self):
        found = resolve('/UploadLicense', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        myUser = Mock()
        myUser.translator = None

        mylfile = Mock()
        mylfile.name = 'a.jpg'

        myLicense = Mock()
        myLicense.name = 'a/b'

        with patch.object(auth,'get_user',return_value = myUser):
            with patch.object(request.FILES,'get',return_value = mylfile):
                with patch.object(request.POST,'get',return_value = 'cet8'):
                    with patch.object(myLicense.licenseImage,'save',return_value = 1):
                        with patch.object(License.objects,'create',return_value= myLicense):
                            response = json.loads(found.func(request).content.decode())
                            self.assertEqual(response['url'], "b")

class ResponseTestResultTestCase(TestCase):
    def test_normal_test_2(self):
        found = resolve('/ResponseTestResult', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        request.body = Mock()
        request.body.decode = Mock(return_value=' {"assignment_id":1,"result":123,"statement":"haha"}')

        myAssignment = Mock()
        myAssignment.status = 2
        myAssignment.translator = 1

        with patch.object(Assignment.objects,'get',return_value = myAssignment):
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response, 0)

    def test_normal_test_1(self):
        found = resolve('/ResponseTestResult', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        request.body = Mock()
        request.body.decode = Mock(return_value=' {"assignment_id":1,"result":123,"statement":"haha"}')

        myAssignment = Mock()
        myAssignment.status = 1
        myAssignment.translator = 1

        with patch.object(Assignment.objects,'get',return_value = myAssignment):
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response, 0)

class SubmitTestResultTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/SubmitTestResult', urlconf = backend.urls)
        request = Mock(wraps=HttpRequest(), method = 'POST')

        request.body = Mock()
        request.body.decode = Mock(return_value=' {"assignment_order":123,"testResult":"haha","task_id":1}')

        myUser = Mock()
        myUser.username = 'shaoyushan'
        myTranslator = Mock()
        myTranslator.translator = myUser

        myAssignment = Mock()
        myAssignment.status = 1
        myAssignment.translator = myUser
        myAssignment.testResult = '123'

        with patch.object(auth,'get_user',return_value = myTranslator):
            with patch.object(Task.objects,'get',return_value = 1):
                with patch.object(Assignment.objects,'get',return_value = myAssignment):
                    response = json.loads(found.func(request).content.decode())
                    self.assertEqual(response['translator'], 'shaoyushan')

class AcceptResultTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/AcceptResult', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        request.body = Mock()
        request.body.decode = Mock(return_value=' {"assignmentId":123,"testResult":"haha","task_id":1}')

        myAssignment = Mock()
        myAssignment.status = 1

        with patch.object(Assignment.objects,'get',return_value = myAssignment):
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['status'], True)

class ArgueResultTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/AcceptResult', urlconf=backend.urls)
        request = Mock(wraps=HttpRequest(), method='POST')

        request.body = Mock()
        request.body.decode = Mock(return_value=' {"assignmentId":123,"testResult":"haha","task_id":1}')

        myAssignment = Mock()
        myAssignment.status = 1

        with patch.object(Assignment.objects, 'get', return_value=myAssignment):
            with patch.object(Dispute.objects,'create',return_value = 1 ):
                response = json.loads(found.func(request).content.decode())
                self.assertEqual(response['status'], True)