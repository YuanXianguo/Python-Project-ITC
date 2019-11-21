# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        db_table = 'user'


class TestResults(models.Model):
    work_pos_id = models.IntegerField()
    sys_time = models.CharField(max_length=20)
    formula = models.CharField(max_length=20)
    test_mode = models.CharField(max_length=20)
    big_leak = models.CharField(max_length=20, blank=True, null=True)
    work_press = models.CharField(max_length=20, blank=True, null=True)
    torque = models.CharField(max_length=20, blank=True, null=True)
    cur_test = models.CharField(max_length=20, blank=True, null=True)
    cur_p1 = models.CharField(max_length=20, blank=True, null=True)
    cur_p2 = models.CharField(max_length=20, blank=True, null=True)
    error_msg = models.CharField(max_length=20, blank=True, null=True)
    is_pass = models.CharField(max_length=5, blank=True, null=True)
    is_delete = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'test_results'
