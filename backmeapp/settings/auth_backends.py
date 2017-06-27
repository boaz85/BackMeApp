import json

from django.core.urlresolvers import reverse

from commons.enums import ServiceTypeEnum
from commons.enums import ProviderEnum
from commons.utilities import Enumeration, Item
from services.services_helpers.GmailHelper import GmailHelper
from services.services_helpers.commons import BaseHelper


class ServicesData(Enumeration):

    class ServiceItem(Item):

        def __get__(self, instance, owner):
            return self

        def __iter__(self):
            for attr in self.__dict__:
                val = getattr(self, attr)
                if not isinstance(val, type):
                    yield (attr, val)

    @classmethod
    def get_serialized(cls):

        for item in cls.__dict__.values():
            if isinstance(item, ServicesData.ServiceItem):
                setattr(item, 'auth_url', reverse('social:begin', args=[item.slug]))
                setattr(item, 'auth_complete', reverse('social:complete', args=[item.slug]))

        items = [dict(item) for item in cls.__dict__.values() if isinstance(item, ServicesData.ServiceItem)]
        return json.dumps([dict(item) for item in cls.__dict__.values() if isinstance(item, ServicesData.ServiceItem)])

    GOOGLE_GMAIL = ServiceItem(order=0,
                               slug='google-gmail',
                               display='Gmail',
                               service_type=ServiceTypeEnum.EMAIL,
                               provider=ProviderEnum.GOOGLE,
                               key='616159569025-chpo79godmuqo52t65fm91gsmd9510di.apps.googleusercontent.com',
                               scope=['profile', 'email', 'https://mail.google.com'],
                               auth_extra_arguments={'access_type': 'offline'},
                               login_redirect_url='/auth-complete/',
                               medium_logo_url='/static/img/logo_gmail_64px.png',
                               helper_class=GmailHelper)

    GOOGLE_SIGNIN = ServiceItem(order=1,
                                slug='google-signin',
                                display='Google Signin',
                                service_type=ServiceTypeEnum.SIGNIN,
                                provider=ProviderEnum.GOOGLE,
                                key='616159569025-ebsgvmqbfvi2umkgu3nspouudggc2p9i.apps.googleusercontent.com',
                                scope=['profile', 'email'],
                                login_redirect_url='/')

    GOOGLE_DRIVE = ServiceItem(order=2,
                               slug='google-drive',
                               display='Google Drive',
                               service_type=ServiceTypeEnum.STORAGE,
                               provider=ProviderEnum.GOOGLE,
                               key='616159569025-gbk7200vr6tkrnvm9b6q0m4a5vv51doj.apps.googleusercontent.com',
                               scope=['profile', 'email', 'https://www.googleapis.com/auth/drive'],
                               auth_extra_arguments={'access_type': 'offline'},
                               login_redirect_url='/auth-complete/',
                               medium_logo_url='/static/img/logo_drive_64px.png')

    DROPBOX = ServiceItem(order=3,
                          slug='dropbox-oauth2',
                          display='Dropbox',
                          service_type=ServiceTypeEnum.STORAGE,
                          provider=ProviderEnum.DROPBOX,
                          key='4wud1nis9lrwxad',
                          login_redirect_url='/auth-complete/',
                          medium_logo_url='/static/img/logo_dropbox_64px.png')