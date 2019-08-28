from rest_framework import serializers
from ..models import Quotes, quote_log
from ..constants import Enum_op, My_Errors
from django.utils import timezone
import logging

# Get an instance of a logger
logger = logging.getLogger('django.request')

class QuotesSerializer(serializers.ModelSerializer):

	def validate(self, data):
		# Make sure that the provided data is valid according to our definition
		# in case that it's not and the DB table will not get updated, 
		# we still log the transaction attempt to our quote_log table
		
		#reqMethod start off as test, so in case of a test-run we will know the reason for that input.
		reqMethod = 'test'
		try:
			if request.method == 'POST':
				reqMethod = Enum_op.CREATE.value
			elif request.method == 'PATCH':
				reqMethod = Enum_op.UPDATE.value
			elif request.method == 'DELETE':
				reqMethod = Enum_op.DELETE.value
			else:
				raise serializers.ValidationError(My_Errors.UnsupportedMethod.value)
		except:
			pass
		latestError = None
		
		# Check for faulty names
		if data["name"].isspace() or len(data["name"]) < 1:
			logger.error(My_Errors.QuoteNameInvalid.value) 
			latestError = My_Errors.QuoteNameInvalid.value
		# And check for faulty Passwords
		elif data['price'] < 0:
			logger.error(My_Errors.QuotePriceBelowZero.value) 
			latestError = My_Errors.QuotePriceBelowZero.value
		# We make it that if any data violation has occured, the last checked violation is persisted to our quote_log audit table.
		if latestError:
			quote_log.objects.create(created_date=timezone.now(),quote_id=data["name"],
												 operation=reqMethod,
												error_code=(latestError['errorCode']), message=(latestError['description']))
			raise serializers.ValidationError(latestError)
		return data
		
	class Meta:
		model = Quotes
		fields="__all__"
		