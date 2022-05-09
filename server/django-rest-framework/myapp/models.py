# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# 참고: https://hyun-am-coding.tistory.com/entry/Django%EB%A5%BC-%EC%9D%B4%EC%9A%A9%ED%95%9C-%EC%9B%B9-API-%EB%A7%8C%EB%93%A4%EA%B8%B0
class Alarm(models.Model):
    aid = models.AutoField(primary_key=True)
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='uid')
    code = models.IntegerField()
    time = models.TimeField()
    onoff = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'alarm'
        unique_together = (('aid', 'uid'),)


class Stock(models.Model):
    code = models.CharField(max_length=50)
    sname = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'stock'


class Trade(models.Model):
    tid = models.AutoField(primary_key=True)
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='uid')
    date = models.DateField()
    price = models.IntegerField()
    count = models.IntegerField()
    buysell = models.CharField(max_length=5)
    code = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'trade'
        unique_together = (('tid', 'uid'),)


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    gid = models.IntegerField()
    uname = models.CharField(max_length=50)
    seed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'
