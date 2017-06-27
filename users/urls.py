from django.conf.urls import url
from django.contrib.auth.views import logout
from services import views
from users.views import is_authorized, user_data

users_patterns = [
    url('is-authorized', is_authorized, name='is-authorized'),
    url('user-data', user_data, name='user-data'),
    url('sign-out', logout, kwargs={'next_page': '/'}, name='logout')
]