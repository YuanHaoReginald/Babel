from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^UserSignUp$', views.UserSignUp, name='UserSignUp'),
    url(r'^UserSignIn$', views.UserSignIn, name='UserSignIn'),
    url(r'^GetUserInfo$', views.GetUserInfo, name='GetUserInfo'),
    url(r'^UserModify$', views.UserModify, name='UserModify'),
    url(r'^UploadAvatar$', views.UploadAvatar, name='UploadAvatar'),
    url(r'^CreateTask$', views.CreateTask, name='CreateTask'),
    url(r'^UploadTaskFile$', views.UploadTaskFile, name='UploadTaskFile'),
    url(r'^GetEmployerTasks$', views.GetEmployerTasks, name='GetEmployerTasks'),
    url(r'^GetTranslatorAssignments$', views.GetTranslatorAssignments, name='GetTranslatorAssignments'),
]
