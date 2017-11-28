from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

	url(r'^TranslatorSignUp$', views.TranslatorSignUp , name='TransloterSignUp'),
    url(r'^UserSignIn$', views.UserSignIn , name='UserSignIn'),
    url(r'^EmployerSignUp$', views.EmployerSignUp , name='EmployerSignUp'),
<<<<<<< HEAD
    url(r'^GetUserInfo$', views.GetUserInfo, name='GetUserInfo'),
=======
    url(r'^UserSignUp$', views.UserSignUp , name='UserSignUp'),
>>>>>>> e110df25a0b137a3c6181ca7deee1d33a10eed70

]
