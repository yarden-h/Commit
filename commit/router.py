from webapp.api.viewsets import QuotesViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('webapp',QuotesViewSet, base_name="webapp")


# for url in router.urls:
	# print(url, '\n')