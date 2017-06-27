import imaplib
# import email
import base64
import io
import logging
from operator import attrgetter
import uu
import binascii
from cStringIO import StringIO
from email import utils
from services.services_helpers.GmailHelper.imapUTF7 import imapUTF7Encode
from services.services_helpers.GmailHelper import bodystructure
from services.services_helpers.commons import BaseEmailHelper, AuthException

GMAIL_IMAP_SERVER = 'imap.gmail.com'
IMAP_DEBUG_LEVEL = 4
AUTH_PROTOCOL = 'XOAUTH2'


class GmailHelper(BaseEmailHelper):
    """
    An helper class for accessing Gmail account
    and retrieving user labels, mails and attachments.
    """

    def __init__(self, username, access_token):
        """
        Constructor

        :param username:
            User name to access his account.

        :param access_token:
            Access token generated using the
            OAuth2 process (not included in this class).
            Used to access user account without password.
        """

        self.username = username
        self.acess_token = access_token
        self.imap_service = imaplib.IMAP4_SSL(GMAIL_IMAP_SERVER)
        self.imap_service.debug = IMAP_DEBUG_LEVEL

    def login(self):
        """
        Login into the user Gmail account
        using his username and access token.
        """
        auth_string = self._generate_oauth2_string(self.username, self.acess_token)
        try:
            rc, response = self.imap_service.authenticate(AUTH_PROTOCOL, lambda x: auth_string)
        except imaplib.IMAP4.error, e:
            raise AuthException()

        logging.debug('Logged in to Gmail as %s' % self.username)

        return rc

    def get_groupers(self):
        return self._format_label_list(self._get_labels())

    def _generate_oauth2_string(self, username, access_token, base64_encode=False):
        """
        Generete OAuth2 string which is necessary
        for connecting to a Gmail account.

        :param username:
            User name to access his account.

        :param access_token:
            Access token generated using the
            OAuth2 process (not included in this class).
            Used to access user account without password.

        :param base64_encode:
            Whether encode auth string to base64 or not.
        """
        auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
        if base64_encode:
            auth_string = base64.b64encode(auth_string)
        return auth_string

    def _get_labels(self):
        """
        Get all user Gmail labels.
        """

        built_in_prefix = "\"[Gmail]/"
        mailboxes = []
        response = map(lambda x: x.strip().strip('"'), self._generate_readable_list(self.imap_service.list()))

        logging.debug('labels retrieved')

        return response

    def _generate_readable_list(self, original_list):
        """
        Genereate a human readable label list

        :para original_list:
            The raw label list.
        """

        readable_list = []
        delimiter = "\"/\""

        for item in original_list[1]:
            label_part = item.split(delimiter)
            readable_list.append(decode(label_part[1]))
        return readable_list

    def _format_label_list(self, user_label_list):
        """
        Parse raw Gmail labels (and sub-labels) data.
        :param user_label_list:
            Raw Gmail labels list.
        """
        labels = []
        exist = {}

        for full_path in user_label_list:
            short_name = full_path.rsplit('/', 1)[-1]
            exist.setdefault(short_name, []).append(full_path)

        for short_name, full_paths in exist.items():

            if len(full_paths) > 1:
                for path in full_paths:

                    splitted = path.rsplit('/', 2)
                    labels.append({'display': '/'.join(splitted[-2:]),
                                   'full_name': path})
            else:
                labels.append({'display': short_name,
                               'full_name': full_paths[0]})

        labels = sorted(labels, cmp=lambda x,y: x['display'] > y['display'])

        return labels

    def select_label(self, label_name):
        """
        Select a specific label.

        :param label_name:
            Label name to select.
        """
        return self.imap_service.select('"' + imapUTF7Encode(label_name) + '"')

    def getLabelUids(self, label_name):
        """
        Get a list of UID's under the specified label.

        :param label_name:
            The label of the UID's to return.
        """
        self.select_label(label_name)
        rc, response = self.imap_service.uid('search', None, "ALL")

        return rc, map(lambda x: int(x), response[0].split())

    def GetMailAttachments(self, label, uid, attachment_extension_list=[]):
        """
        Get attachments of the specified mail.

        :param label:
            The label of the mail.

        :param uid:
            The uid of the mail.

        :param attachment_extension_list:
            Allow filtering only specified file types.
        """
        self.select_label(label)
        rc, body = self.imap_service.uid('fetch', uid, 'BODY')

        if rc != 'OK':
            raise Exception('FETCH FAILED!')
        # TODO: handle this

        body = body[0]
        body = '(' + body[body.find('BODY'):]

        parts = bodystructure.parse_bodystructure(body)

        for part in parts:

            if '"NAME"' not in part: continue

            divided_part = part.strip().split()

            divided_stripped = map(lambda x: x.strip('"'), divided_part)

            file_name = divided_stripped[4].strip(')').strip('"')

            if attachment_extension_list and file_name.split('.')[-1] not in attachment_extension_list: continue

            body = {'title': file_name,
                    'description': 'This file was uploaded using BackMeApp',
                    'mimeType': (divided_stripped[1] + '/' + divided_stripped[2]).lower()}

            part_num = divided_stripped[0].split('.')[0]

            rc, file_data = self.imap_service.uid('fetch', uid, '(BODY[%s])' % part_num)

            file_data = file_data[0][1]

            if '.' in divided_stripped[0]:
                file_str = 'Content-ID: <%s>\r\n\r\n' % file_name

                file_data = file_data[file_data.find(file_str) + len(file_str):]
                file_data = file_data[:file_data.find('=') + 1]

            file_data = io.BytesIO(self.decode_payload(divided_stripped[7], file_data))

            yield [body, file_data]

    def decode_payload(self, encoding, payload):
        """
        Decode attachment payload data.

        :param encoding:
            The current encoding of the payload data.

        :param payload:
            the payload data
        """
        cte = encoding.lower()
        if cte == 'quoted-printable':
            return utils._qdecode(payload)
        elif cte == 'base64':
            try:
                return utils._bdecode(payload)
            except binascii.Error:
                # Incorrect padding
                return payload
        elif cte in ('x-uuencode', 'uuencode', 'uue', 'x-uue'):
            sfp = StringIO()
            try:
                uu.decode(StringIO(payload + '\n'), sfp, quiet=True)
                payload = sfp.getvalue()
            except uu.Error:
                # Some decoding problem
                return payload

    def get_mail_by_id(self, id):
        """
        Get a specific mail by uid.

        :param id:
            The uid of the mail to get.
        """
        status, response = self.imap_service.fetch(id, '(body[header.fields (subject)])')
        return response

    def logout(self):
        """
        Log out from the gmail account.
        """
        self.imap_service.close()
        self.imap_service.logout()


def decode(s):
    r = []
    decode = []
    for c in s:
        if c == '&' and not decode:
            decode.append('&')
        elif c == '-' and decode:
            if len(decode) == 1:
                r.append('&')
            else:
                r.append(modified_unbase64(''.join(decode[1:])))
                decode = []
        elif decode:
            decode.append(c)
        else:
            r.append(c)
    if decode:
        r.append(modified_unbase64(''.join(decode[1:])))
    out = ''.join(r)

    if not isinstance(out, unicode):
        out = unicode(out, 'latin-1')
    return out


def modified_base64(s):
    s_utf7 = s.encode('utf-7')
    return s_utf7[1:-1].replace('/', ',')


def modified_unbase64(s):
    s_utf7 = '+' + s.replace(',', '/') + '-'
    return s_utf7.decode('utf-7')
