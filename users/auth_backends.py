import base64
import crypt
import hashlib

from django.utils.crypto import constant_time_compare
from oauth2client import client
from backmeapp import settings
from backmeapp.settings import ServicesData

from social.backends.google import GoogleOAuth2, GooglePlusAuth
from social.exceptions import AuthMissingParameter, AuthCanceled, AuthFailed

class GoogleDriveBackend(GoogleOAuth2):

    name = ServicesData.GOOGLE_DRIVE.slug


class GoogleGmailBackend(GoogleOAuth2):

    name = ServicesData.GOOGLE_GMAIL.slug


class GoogleSignInBackend(GooglePlusAuth):

    name = ServicesData.GOOGLE_SIGNIN.slug

    def auth_complete(self, *args, **kwargs):

        if 'idtoken' not in self.data:
            raise AuthMissingParameter(self, 'idtoken')

        if 'access_token' not in self.data:
            raise AuthMissingParameter(self, 'access_token')

        try:
            idinfo = client.verify_id_token(self.data['idtoken'], settings.SOCIAL_AUTH_GOOGLE_SIGNIN_KEY)
            # If multiple clients access the backend server:
            if idinfo['aud'] != settings.SOCIAL_AUTH_GOOGLE_SIGNIN_KEY:
                raise crypt.AppIdentityError("Unrecognized client.")
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")

        except crypt.AppIdentityError, e:
            raise AuthFailed(self, str(e))

        hash = hashlib.sha256()
        hash.update(self.data["access_token"])
        digest = hash.digest()
        digest_truncated = digest[:16]
        at_hash_computed = base64.urlsafe_b64encode(digest_truncated).rstrip(b'=')

        if not constant_time_compare(at_hash_computed, idinfo['at_hash']):
            raise AuthCanceled(self, 'Invalid access token')

        return self.do_auth(self.data["access_token"], *args, **kwargs)