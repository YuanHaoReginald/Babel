from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

	url(r'^TranslatorSignUp$', views.TranslatorSignUp , name='TransloterSignUp'),
    url(r'^UserSignIn$', views.UserSignIn , name='UserSignIn'),
    url(r'^EmployerSignUp$', views.EmployerSignUp , name='EmployerSignUp'),
    url(r'^UserSignUp$', views.UserSignUp , name='UserSignUp'),

]
