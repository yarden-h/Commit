from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "main"

urlpatterns = [
	url(r'^$', views.index, name = 'index'), # the index page.
	url(r'^register/$', views.register, name = 'register'),
	url(r'^logout/$', views.logout_request, name = 'logout'),
	url(r'^login/', views.login_request, name = 'login'),
	#url(r'^quotes/$', views.QuotesList.as_view()),
]
