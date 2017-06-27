
class AuthException(Exception):
    pass

class BaseHelper(object):

    def login(self, *args, **kwargs):
        raise NotImplemented()


class BaseEmailHelper(BaseHelper):

    def get_groupers(self):
        raise NotImplemented()

