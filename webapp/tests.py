from django.test import TestCase, Client
from .models import Quotes
from .api.serializers import QuotesSerializer
from urllib.parse import urlencode

from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class QuotesTest(APITestCase):
	
	""" Test module for Quotes model """
	
	def setUp(self):
		# Set up the client and create a user so we can get a token
		self.client = APIClient()
		self.user = User.objects.create_superuser('admin', 'admin@admin.com', 'admin123')
		self.token = Token.objects.create(user=self.user)
		
		self.url = "http://localhost:8000/api/webapp/"
		
	
	def testQuotesValidations(self):
		# Get the token so we can send CRUD requests
		request = self.client.post('/api-token-auth/', {'username': 'admin', 'password': 'admin123'})
		token = "Token " + request.data['token']
		
		
		# JSONdata will be defined a few time, this is the data we validate in this test.
		# validations required: no negative price, and no empty names, I have also added a name duplicate validation test.
		
		# Negative price validation
		JSONdata = {"name": "quote1","price": -6,"items": [{"name": "SOME ITEM","id": 0}]}
		
		# let the serializer validate JSONdata
		serializer = QuotesSerializer(data=JSONdata)
		#Check the results...
		self.assertEqual(serializer.is_valid(), False)
		
		# Empty name validation
		JSONdata = {"name": "","price": 5,"items": [{"name": "SOME ITEM","id": 0}]}
		
		serializer = QuotesSerializer(data=JSONdata)
		self.assertEqual(serializer.is_valid(), False)
		request = self.client.post(self.url, data=JSONdata, format='json', HTTP_AUTHORIZATION=token)
		
		
		# Duplicate name validation
		JSONdata = {"name": "quote1","price": 65,"items": [{"name": "SOME ITEM","id": 0}]}
		
		serializer = QuotesSerializer(data=JSONdata)
		self.assertEqual(serializer.is_valid(), True)
		request = self.client.post(self.url, data=JSONdata, format='json', HTTP_AUTHORIZATION=token)
		
		serializer = QuotesSerializer(data=JSONdata)
		self.assertEqual(serializer.is_valid(), False)
