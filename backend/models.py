from django.db import models
from django.contrib.auth.models import AbstractUser

# Base User
class User(AbstractUser):
    email = models.CharField(max_length=100, unique=True, null=True)
    avatar = models.ImageField(max_length=256, null=True)
    utype = models.CharField(max_length=30)

# admin user
class Admin(User):
    pass


# Commen User
class CommenUser(User):
    creditLevel = models.FloatField(default=3)
    experience = models.IntegerField(default=0)
    alipayNumber = models.CharField(max_length=30, null=True)
    wechatNumber = models.CharField(max_length=30, null=True)

    class Meta:
        abstract = True


# translator
class Translator(CommenUser):
    # wechatNumber = models.CharField(max_length=30, null=True)
    pass

# employer
class Employer(User):
    # wechatNumber = models.CharField(max_length=30, null=True)
    pass

# task table
class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=512, null=True)
    fileUrl = models.FileField(max_length=256)
    fileType = models.IntegerField()  # 0:文本；1:音频; 2:视频; 3:其他
    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE
    )
    # time
    publishTime = models.DateTimeField()
    ddlTime = models.DateTimeField()
    # tags
    languageOrigin = models.IntegerField()
    languageTarget = models.IntegerField()
    requirementLicense = models.IntegerField(null=True)
    requirementCreditLevel = models.IntegerField(null=True)
    testText = models.TextField(max_length=1000, null=True)
    testResult = models.TextField(max_length=1000, null=True)

class Tag(models.Model):
    tag = models.CharField(max_length=128, unique=True)
    task = models.ManyToManyField(Task)

#  Assignments
class Assignment(models.Model):
    description = models.TextField(max_length=1000)
    # (saved：0/published：1/running：2/finished：3/arguing：4)
    status = models.IntegerField(default=0)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    order = models.IntegerField()
    translator = models.ForeignKey(Translator, null=True, on_delete=models.CASCADE)
    scores = models.FloatField(null=True)
    price = models.IntegerField(null=True)
    submission = models.FileField(max_length=256, null=True)
    experience = models.IntegerField(default=0)

# dispute
class Dispute(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    employerStatement = models.TextField(max_length=1000, null=True)
    translatorStatement = models.TextField(max_length=1000, null=True)
    status = models.IntegerField()  # 0:未处理；1：已处理
    adminStatement = models.TextField(max_length=1000, null=True)


# language type
# CHINESE = 0
# ENGLISH = 1
# JAPANESE = 2
# FRENCH = 3
# RUSSIAN = 4
# SPAINISH = 5

# language
class Language(models.Model):
    languageType = models.IntegerField()
    TranslatorId = models.ManyToManyField(Translator)

# license type
# CET4 = 0
# CET6 = 1
# TOFEL100 = 2
# TOFEL110 = 3

# license
class License(models.Model):
    licenseType = models.IntegerField()
    licenseImage = models.ImageField(max_length=256)
    description = models.CharField(max_length=100, null=True)
    belonger = models.ManyToManyField(Translator)
    adminVerify = models.BooleanField(default=False)
