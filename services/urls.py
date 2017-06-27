from django.conf.urls import url
from services import views

services_patterns = [
    url(r'services-data/$', views.services_data, name='services-data'),
    url(r'email-groupers', views.user_email_groupers, name='email-groupers')
]