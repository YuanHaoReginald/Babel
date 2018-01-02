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

        #print(user_employer.telephone)

        request = Mock(wraps = HttpRequest(), method = 'GET')
        request.body = Mock()
        request.body.decode = Mock(return_value='{"telephone":"13333333333","alipayNumber":"alipay","wechatNumber":"wechat","utype":"employer"}')

        with patch.object(auth, 'get_user', return_value=Mock(employer = user_employer, utype = 'employer')) as MockUser:
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['telephone'], '13333333333')

class UploadAvatarTestCase(TestCase):
    def test_normal_test(self):
        found = resolve('/UploadAvatar', urlconf = backend.urls)

        myavatar = Mock(name = 'a.jpg')
        request = Mock(wraps=HttpRequest(), method='POST')
        request.FILES = Mock(avatar = myavatar)

        with patch.object(auth, 'get_user', return_value=Mock(username = 'shaoyushan', avatar = myavatar)) as MockUser:
            response = json.loads(found.func(request).content.decode())
            self.assertEqual(response['url'], 'shaoyushan.jpg')


