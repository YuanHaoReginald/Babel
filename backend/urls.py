from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^UserSignUp$', views.UserSignUp, name='UserSignUp'),
    url(r'^UserSignIn$', views.UserSignIn, name='UserSignIn'),
    url(r'^UsernameCheck$', views.UsernameCheck, name='UsernameCheck'),
    url(r'^UserLogout$', views.UserLogout, name='UserLogout'),
    url(r'^GetUserInfo$', views.GetUserInfo, name='GetUserInfo'),
    url(r'^UserModify$', views.UserModify, name='UserModify'),
    url(r'^UploadAvatar$', views.UploadAvatar, name='UploadAvatar'),
    url(r'^CreateTask$', views.CreateTask, name='CreateTask'),
    url(r'^UploadTaskFile$', views.UploadTaskFile, name='UploadTaskFile'),
    url(r'^GetEmployerTasks$', views.GetEmployerTasks, name='GetEmployerTasks'),
    url(r'^GetTranslatorAssignments$', views.GetTranslatorAssignments, name='GetTranslatorAssignments'),
    url(r'^PickupAssignment$', views.PickupAssignment, name='PickupAssignment'),
    url(r'^GetTaskDetail$', views.GetTaskDetail, name='GetTaskDetail'),
    url(r'^GetAssignmentDetail$', views.GetAssignmentDetail, name='GetAssignmentDetail'),
    url(r'^GetSquareTasks$', views.GetSquareTasks, name='GetSquareTasks'),
    url(r'^PublishTask$', views.PublishTask, name='PublishTask'),
    url(r'^SubmitAssignment$', views.SubmitAssignment, name='SubmitAssignment'),
    url(r'^SolveDispute$', views.SolveDispute, name='SolveDispute'),
    url(r'^VerifyLicense$', views.VerifyLicense, name='VerifyLicense'),
    url(r'^GetManager$', views.GetManager, name='GetManager'),
    url(r'^AcceptAssignment$', views.AcceptAssignment, name='AcceptAssignment'),
    url(r'^FileDownload$', views.FileDownload, name='FileDownload'),
    url(r'^UploadLicense$', views.UploadLicense, name='UploadLicense'),
    url(r'^ResponseTestResult$', views.ResponseTestResult, name='ResponseTestResult'),
    url(r'^SubmitTestResult$', views.SubmitTestResult, name='SubmitTestResult'),
    url(r'^AcceptResult$', views.AcceptResult, name='AcceptResult'),
    url(r'^ArgueResult$', views.ArgueResult, name='ArgueResult'),
]
