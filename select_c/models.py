from django.db import models
# Create your models here.

class user(models.Model):
    userid = models.CharField(max_length=20,primary_key=True,default='')
    password = models.CharField(max_length=20)
class S(models.Model):
    sid = models.CharField(max_length=20,primary_key=True)
    sname = models.CharField(max_length=20)
    sex = models.CharField(max_length=20)
    academy = models.CharField(max_length=40)
    age = models.CharField(max_length=20)
class T(models.Model):
    tid = models.CharField(max_length=20,primary_key=True)
    tname = models.CharField(max_length=20)
    sex = models.CharField(max_length=20)
    academy = models.CharField(max_length=40)
    age = models.CharField(max_length=20)
class O(models.Model):
    cid = models.CharField(max_length=20,primary_key=True)
    cname = models.CharField(max_length=40)
    credit = models.IntegerField(default=0)
    academy = models.CharField(max_length=40)
    tname = models.CharField(max_length=20)
    tid = models.CharField(max_length=20)
    test = models.FloatField(default=0)
    normal = models.FloatField(default=0)
class E(models.Model):
    sid = models.CharField(max_length=20)
    sname = models.CharField(max_length=20,default='')
    cid = models.CharField(max_length=20)
    cname = models.CharField(max_length=40,default='')
    tid = models.CharField(max_length=20)
    tname = models.CharField(max_length=20,default='')
    pscj= models.FloatField(default=0)
    kscj= models.FloatField(default=0)
    zpcj= models.FloatField(default=0)