from django.db import models
from django.contrib.auth.models import User

# Base User
class CommonUser(User):
    telephone = models.CharField(max_length = 20, unique = True)
    avatar = models.ImageField(max_length = 256)
    utype = models.CharField(max_length = 30)

# admin user
class Admin(CommonUser):
    pass

# translator
class Translator(CommonUser):
    level = models.IntegerField()
    alipayNumber = models.CharField(max_length = 30, null = True)
    wechatNumber = models.CharField(max_length = 30, null = True)
    experience = models.IntegerField(default = 0)

# employer
class Employer(CommonUser):
    level = models.IntegerField(default = 0)
    alipayNumber = models.CharField(max_length = 30, null = True)
    wechatNumber = models.CharField(max_length = 30, null = True)
    experience = models.IntegerField(default = 0)

# task table
class Task(models.Model):
    title = models.CharField(max_length = 30)
    description = models.CharField(max_length = 512)
    fileUrl = models.FileField(max_length = 256)
    fileType = models.IntegerField() # 0:文本；1:音频
    employer = models.ForeignKey(Employer)
    # time
    publishTime = models.DateTimeField()
    ddlTime = models.DateTimeField()
    # tags
    tags = models.CharField(max_length = 128, null = True)
    language = models.IntegerField()
    requirementsLicense = models.IntegerField()
    requirementsLevel = models.IntegerField()
    testText = models.TextField(max_length = 300, null = True)

#  Assignments
class Assignment(models.Model):
    # (saved：0/published：1/running：2/finished：3/submitted：4/arguing：5)
    status = models.IntegerField()
    task = models.ForeignKey(Task)
    testTextFinished = models.TextField(max_length = 1000)
    translator = models.ForeignKey(Translator)
    scores = models.IntegerField()
    price = models.IntegerField()
    submission = models.FileField(max_length = 50)
    experience = models.IntegerField()

# dispute
class Dispute(models.Model):
    assignment = models.ForeignKey(Assignment)
    employerStatement = models.TextField(max_length = 1000)
    translatorStatement = models.TextField(max_length = 1000)
    status = models.IntegerField() #0:未处理；1：已处理
    adminStatement = models.TextField(max_length = 1000)

#language type
CHINESE = 0
ENGLISH = 1
JAPANESE = 2
FRENCH = 3
RUSSIAN = 4
SPAINISH = 5
# language
class Language(models.Model):
    languageType = models.IntegerField()
    TranslatorId = models.ForeignKey(Translator)
    @classmethod
    def get_by_translatorId(cls,transId):
        try:
            return cls.objects.filter(translatorId = transId)
        except cls.DoesNotExist:
            #raise LogicError('User not found')
            return

#license type
CET4 = 0
CET6 = 1
TOFEL100 = 2
TOFEL110 = 3

class License(models.Model):
    licenseType = models.IntegerField()
    licenseImage = models.ImageField(max_length = 256)
    description = models.CharField(max_length = 100)
    belonger = models.ForeignKey(Translator)

    @classmethod
    def get_by_belongerId(cls,transId):
        try:
            return cls.objects.filter(belonger = transId)
        except cls.DoesNotExist:
            #raise LogicError('User not found')
            return










