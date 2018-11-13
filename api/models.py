# coding:utf-8
from django.db import models


# Create your models here.

class Meeting(models.Model):
    title = models.CharField(max_length=64, null=False, unique=True)
    address = models.CharField(max_length=64, null=False)
    time = models.DateTimeField()
    limit = models.IntegerField(null=True, default=200)
    status = models.IntegerField(choices=((0, '未开始'), (1, '进行中'), (2, '已结束')), null=True, default=0)


class Guest(models.Model):
    name = models.CharField(max_length=32, null=False)
    phone_number = models.CharField(max_length=16, null=False, unique=True)
    email = models.EmailField(max_length=64, null=True)
    meeting = models.ManyToManyField(Meeting)
