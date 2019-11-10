from django.db import models

# Create your models here.


class AccntInfo(models.Model):
    accnt_num = models.IntegerField(db_column='accnt_num', primary_key=True)
    user_name = models.CharField(db_column='user_name', max_length=45)
    user_passwd = models.CharField(db_column='user_passwd',max_length=45)
    bal = models.IntegerField(db_column='bal')
    is_valid = models.IntegerField(db_column='is_valid')

    class Meta:
        managed = False
        db_table = 'accnt_info'


class StaffInfo(models.Model):
    staff_id = models.CharField(db_column='staff_id', max_length=45, primary_key=True)
    staff_passwd = models.CharField(db_column='staff_passwd',max_length=45)


    class Meta:
        managed = False
        db_table = 'staff_info'


class TransInfo(models.Model):
    trans_num = models.IntegerField(db_column='trans_num', primary_key=True)
    source_accnt = models.IntegerField(db_column='source_accnt')
    dest_accnt = models.IntegerField(db_column='dest_accnt')
    amnt = models.IntegerField(db_column='amnt')

    class Meta:
        managed = False
        db_table = 'trans_info'
