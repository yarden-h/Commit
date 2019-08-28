from django.db import models
from django.contrib.postgres.fields.jsonb import JSONField as JSONBField
from django.contrib.postgres.fields import ArrayField

class Quotes(models.Model):
	name = models.CharField(max_length=50,unique=True)
	price = models.BigIntegerField()
	items = ArrayField(base_field=JSONBField(default=list,null=False,blank=True),null=False)
	deleted = models.BooleanField(default=False)
	
		
	def __str__(self):
		return self.name

class quote_log(models.Model):
	created_date = models.DateField()
	quote_id = models.CharField(max_length=50)
	operation = models.CharField(max_length=50)
	error_code = models.BigIntegerField(default=0)
	message = models.TextField(default="No error")
	
	def __str__(self):
		return self.name
