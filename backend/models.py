from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Base User
class User(AbstractUser):
    email = models.CharField(max_length=100, unique=True, null=True)
    avatar = models.ImageField(max_length=256, null=True)
    utype = models.CharField(max_length=30)

# admin user
class Admin(User):
    pass

# Commen User
class CommonUser(User):
    creditLevel = models.FloatField(default=3)
    experience = models.IntegerField(default=0)
    telephone = models.CharField(max_length=20, unique=True, null=True)
    alipayNumber = models.CharField(max_length=30, null=True)
    wechatNumber = models.CharField(max_length=30, null=True)

    class Meta:
        abstract = True

# translator
class Translator(CommonUser):
    # wechatNumber = models.CharField(max_length=30, null=True)
    pass

# employer
class Employer(CommonUser):
    # wechatNumber = models.CharField(max_length=30, null=True)
    pass

# task table
class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=512, null=True)
    # (saved：0/published&running：1/closed：2)
    status = models.IntegerField(default=0)
    fileUrl = models.FileField(max_length=256, null=True)
    fileType = models.IntegerField()  # 0:文本；1:音频; 2:视频; 3:其他
    employer = models.ForeignKey(
        Employer, on_delete=models.CASCADE
    )
    # time
    publishTime = models.DateTimeField(default=timezone.now)
    ddlTime = models.DateTimeField()
    languageOrigin = models.IntegerField(default = 0)
    languageTarget = models.IntegerField()
    requirementLicense = models.IntegerField(null=True)
    requirementCreditLevel = models.FloatField(null=True)
    testText = models.TextField(max_length=1000, null=True)


class Tag(models.Model):
    tag = models.CharField(max_length=128, unique=True)
    tasks = models.ManyToManyField(Task)

class Assignment(models.Model):
    description = models.TextField(max_length=1000)
    # (saved：0/published：1/running：2/finished：3/arguing：4/tryTranslate: 10)
    status = models.IntegerField(default=0)
    testResult = models.TextField(max_length=1000, null=True)    
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    order = models.IntegerField()
    translator = models.ForeignKey(Translator, null=True, on_delete=models.CASCADE)
    scores = models.FloatField(null=True)
    comment = models.TextField(null=True)
    price = models.IntegerField(null=True)
    submission = models.FileField(max_length=256, null=True)
    experience = models.IntegerField(default=0)

# dispute
class Dispute(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    employerStatement = models.TextField(max_length=1000, null=True)
    translatorStatement = models.TextField(max_length=1000, null=True)
    status = models.IntegerField(default=0)  # 0:未处理；1：TranslatorSide 2: EmployerSide
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
    translators = models.ManyToManyField(Translator)

# license type
# CET4 = 0
# CET6 = 1
# TOFEL100 = 2
# TOFEL110 = 3
# license
class License(models.Model):
    licenseType = models.IntegerField()
    licenseImage = models.ImageField(max_length=256, null=True)
    belonger = models.ForeignKey(Translator, on_delete=models.CASCADE)
    adminVerify = models.IntegerField(default=0) # 0:未处理；1：有效 2: 无效
