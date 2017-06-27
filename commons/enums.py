import json
from django.core.urlresolvers import reverse_lazy, reverse
from commons.utilities import Enumeration
from commons.utilities import Item



class ApiEnum(Enumeration):

    GMAIL = Item(0, 'gmail', 'Gmail')

    DRIVE = Item(1, 'drive', 'Google Drive')


class ProviderEnum(Enumeration):

    GOOGLE = Item(0, 'google', 'Google')

    DROPBOX = Item(1, 'dropbox', 'Dropbox')


class ServiceTypeEnum(Enumeration):

    EMAIL = Item(0, 'email', 'Email')

    STORAGE = Item(1, 'storage', 'Storage')

    SIGNIN = Item(2, 'signin', 'Sign In')

