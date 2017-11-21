from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

	url(r'^TranslaterSignUp$', views.TranslaterSignUp , name='TranslaterSignUp'),
    url(r'^TranslaterSignIn$', views.TranslaterSignIn , name='TranslaterSignIn'),

]