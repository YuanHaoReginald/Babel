from django.db import models
from django.contrib.auth.models import User

# Base User
class CommonUser(User):
    telephone = models.CharField(max_length = 20, unique = True,null = True)
    avatarImageUrl = models.ImageField(max_length = 256 , null = True)
    utype = models.CharField(max_length = 30)

# admin user
class Admin(CommonUser):
    pass

# translator
class Translator(CommonUser):
    level = models.IntegerField(null = True)
    alipayNumber = models.CharField(max_length = 30 , null = True)
    wechatNumber = models.CharField(max_length = 30, null = True)
    experienceNumber = models.IntegerField( null = True)

# employer
class Employer(CommonUser):
    level = models.IntegerField(null = True)
    alipayNumber = models.CharField(max_length = 30, null = True)
    wechatNumber = models.CharField(max_length = 30, null = True)
    experienceNumber = models.IntegerField(null = True)

# task table
class Task(models.Model):
    title = models.CharField(max_length = 30)
    description = models.CharField(max_length = 512)
    fileUrl = models.FileField(max_length = 256)
    fileType = models.IntegerField() # 0:文本；1:音频
    employerId = models.ForeignKey(Employer, related_name = 'partyA', null = True)
    # time
    publishTime = models.DateTimeField()
    ddlTime = models.DateTimeField()
    # tags
    tags = models.CharField(max_length = 128 , null = True)
    language = models.IntegerField( null = True)
    requirementsLicense = models.IntegerField( null = True)

    requirementsLevel = models.IntegerField( null = True)
    testText = models.TextField(max_length = 300, null = True)

#  Assignments
class Assignment(models.Model):
    # (saved：0/published：1/running：2/finished：3/submitted：4/arguing：5)
    status = models.IntegerField()
    task = models.ForeignKey(Task)
    testTextFinished = models.TextField(max_length = 600, null = True)
    translator = models.ForeignKey(Translator, related_name = 'partyB', null = True)
    scores = models.IntegerField( null = True)
    price = models.IntegerField( null = True)
    submission = models.FileField(max_length = 50, null = True)
    experience = models.IntegerField(null = True)

# dispute
class Dispute(models.Model):
    assignment = models.ForeignKey(Assignment)
    employerStatement = models.TextField(max_length = 1000, null = True)
    translatorStatement = models.TextField(max_length = 1000, null = True)
    status = models.IntegerField() #0:未处理；1：已处理
    adminStatement = models.TextField(max_length = 1000, null = True)

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

# license type
CET4 = 0
CET6 = 1
TOFEL100 = 2
TOFEL110 = 3

# license
class License(models.Model):
    licenseType = models.IntegerField()
    licenseImage = models.ImageField(max_length = 256, null = True)
    description = models.CharField(max_length = 100, null = True)
    belonger = models.ForeignKey(Translator)
    adminVerify = models.BooleanField( null = True)
    @classmethod
    def get_by_belongerId(cls,transId):
        try:
            return cls.objects.filter(belonger = transId, adminVerify = True)
        except cls.DoesNotExist:
            #raise LogicError('User not found')
            return










