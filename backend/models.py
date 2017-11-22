from django.db import models

# admin user
class Admin(models.Model):
    username = models.CharField(max_length = 20, unique=True, db_index=True)
    password = models.CharField(max_length = 20, unique=True)
    telephone = models.CharField(max_length = 20, unique = True)
    email = models.CharField(max_length = 20, unique = False)
    avatarImageUrl = models.ImageField(max_length = 256)

# translater
class Translater(models.Model):
    username = models.CharField(max_length = 20, unique=True, db_index=True)
    password = models.CharField(max_length = 20)
    telephone = models.CharField(max_length = 20)
    email = models.CharField(max_length = 20, unique = False)
    avatarImageUrl = models.ImageField(max_length = 256)
    level = models.IntegerField()

    # 在license和language里实现了两个方法，输入translaterId返回它们各自的license表和language表

    alipayNumber = models.CharField(max_length = 30)
    wechatNumber = models.CharField(max_length = 30)
    experienceNumber = models.IntegerField()

# employer
class Employer(models.Model):
    username = models.CharField(max_length = 20, unique=True, db_index=True)
    password = models.CharField(max_length = 20, unique=True)
    telephone = models.CharField(max_length = 20, unique = True)
    email = models.CharField(max_length = 20, unique = False)
    avatarImageUrl = models.ImageField(max_length = 256)

    level = models.IntegerField()
    experienceNumber = models.IntegerField()
    alipayNumber = models.CharField(max_length = 30)
    wechatNumber = models.CharField(max_length = 30)

# task table
class Task(models.Model):
    title = models.CharField(max_length = 30, unique=True)
    description = models.CharField(max_length = 100, unique=True)
    fileUrl = models.FilePathField(max_length = 256)
    fileType = models.IntegerField() # 0:文本；1:音频
    # 甲方
    employerId = models.IntegerField()
    # time
    publishTime = models.DateTimeField()
    ddlTime = models.DateTimeField()

    # tags
    tags = models.CharField(max_length = 128)
    language = models.IntegerField()
    requirementsLicense = models.IntegerField()

    requirementsLevel = models.IntegerField()
    testText = models.TextField(max_length = 300)

#  Assignments
class Assignment(models.Model):
    # (saved：0/published：1/running：2/finished：3/submitted：4/arguing：5)
    status = models.IntegerField()
    testTextFinished = models.TextField(max_length = 600)
    traslaterId = models.IntegerField()
    scores = models.IntegerField()
    price = models.IntegerField()
    submissionFileUrl = models.CharField(max_length = 50)
    experience = models.IntegerField()

# dispute
class Dispute(models.Model):
    taskId = models.IntegerField()
    assignmentId = models.IntegerField()
    employerStatement = models.CharField(max_length = 300)
    translaterStatement = models.CharField(max_length = 300)
    status = models.IntegerField()#0:未处理；1：已处理
    adminStatement = models.CharField(max_length = 300)

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
    translaterId = models.ForeignKey(Translater)

    @classmethod
    def get_by_translaterId(cls,transId):
        try:
            return cls.objects.filter(translaterId = transId)
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
    belonger = models.ForeignKey(Translater)

    @classmethod
    def get_by_belongerId(cls,transId):
        try:
            return cls.objects.filter(belonger = transId)
        except cls.DoesNotExist:
            #raise LogicError('User not found')
            return










