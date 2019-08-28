from webapp.models import Quotes, quote_log
from .serializers import QuotesSerializer
from webapp.constants import Enum_op, My_Errors
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.http import JsonResponse

import logging

# Get an instance of a logger
logger = logging.getLogger('django.request')



class QuotesViewSet(viewsets.ModelViewSet):
	
	# queryset is the default GET response
	# authentication_classes and permission_classes make sure that the request has an authentication token
	queryset = Quotes.objects.filter(deleted=False)
	serializer_class = QuotesSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

	def create(self, request): 
		# Responds to a POST request.
		
		# Check if provided quote name already exists in the database in order to prevent duplicates.
		if Quotes.objects.filter(name=request.data["name"]).exists():
			# Log to our log file and audit table.
			logger.error(My_Errors.QuoteExists.value)
			quote_log.objects.create(created_date=timezone.now(),quote_id=request.data["name"],
												 operation=Enum_op.CREATE.value,
												error_code=(My_Errors.QuoteExists.value['errorCode']), message=(My_Errors.QuoteExists.value['description']))
			return Response(My_Errors.QuoteExists.value)
			
		# Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes
		# And they also validate our data (with custom validations I made.)
		serializer = QuotesSerializer(data=request.data)
		serializer.is_valid()
		serializer.validate(request.data)
		
		# Create new quote, and log the transaction into the quote_log table.
		quer = Quotes.objects.create(name=request.data["name"], price=request.data["price"], items=request.data["items"])
		quote_log.objects.create(created_date=timezone.now(),quote_id=request.data["name"], operation=Enum_op.CREATE.value)
		return Response(serializer.data)
	
	def patch(self, request):
		# Responds to a PATCH request.
		
		serializer = QuotesSerializer(data=request.data)
		serializer.validate(request)
		
		# Update quote, and log the transaction into the quote_log table.
		quer = Quotes.objects.filter(name=request.data["name"]).update(price=request.data['price'])
		quote_log.objects.create(created_date=timezone.now(),quote_id=request.data["name"], operation=Enum_op.UPDATE.value)
		return Response({"status": 200})

	def delete(self, request):
		# Responds to a DELETE request.
		
		serializer = QuotesSerializer(data=request.data)
		serializer.validate(request)
		# Delete quote using soft deletion, and log the transaction into the quote_log table.
		Quotes.objects.filter(name=request.data["name"]).update(deleted=True)
		quote_log.objects.create(created_date=timezone.now(),quote_id=request.data["name"], operation=Enum_op.DELETE.value)
		return Response({"status": 200})