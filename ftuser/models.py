from operator import mod
from tabnanny import verbose
from django.db import models
import uuid

# Create your models here.

class Ftuser(models.Model):
	userid = models.CharField(max_length=64, verbose_name='유저ID', primary_key=True)
	email = models.EmailField(verbose_name='이메일')
	password = models.CharField(max_length=300, verbose_name='비밀번호')
	register_date = models.DateTimeField(auto_now_add=True, verbose_name='등록날짜')

	def __str__(self):
		return self.userid

	class Meta:
		db_table = 'cryptolab_ftuser'
		verbose_name = '사용자'
		verbose_name_plural = '사용자'

class UserLocation(models.Model):
	id = models.ForeignKey('Ftuser', models.DO_NOTHING, max_length=64, blank=True, null=True, db_column='id')
	qrcode = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False)
	latitude = models.FloatField(null=False)
	longitude = models.FloatField(null=False)
	isval = models.BooleanField(default=True, null=False)

	class Meta:
		db_table = 'cryptolab_location'
		verbose_name = 'QR'
		verbose_name_plural = 'QR'
