from django.test import TestCase
from django.test.client import Client
from .views import *
from .models import *
from django.core.urlresolvers import resolve
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from unittest.mock import Mock,patch
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
        myuser = Mock()
        myuser.username = 'shaoyushan'
        myuser.avatar = myavatar

        with patch.object(request.FILES,'get',return_value = myavatar):
            with patch.object(auth, 'get_user', return_value = myuser) as MockUser:
                response = json.loads(found.func(request).content.decode())
                self.assertEqual(response['url'], 'a.jpg')


class CreateTaskTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/CreateTask', urlconf = backend.urls)
        request = Mock(wraps= HttpRequest() , method = 'POST')
        request.body = Mock()
        request.body.decode = Mock(return_value = ' {"title":"a title","description":"a des","language":"French","license":"TOFEL100","level":2.1,"tags":"123","ddlTime":123456.23,"assignments":[{"order":123,"text":"asd"}] }')
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


# class GetEmployerTasksTestCase(TestCase):
#     def test_normal_test(self):
#         found = resolve('/GetEmployerTasks', urlconf=backend.urls)
#         request = Mock(wraps=HttpRequest(), method='GET')

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
