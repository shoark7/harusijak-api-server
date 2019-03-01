from django.utils.translation import ugettext_lazy as _

from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import get_authorization_header, TokenAuthentication


class CustomTokenAuthentication(TokenAuthentication):
    keyword = ''

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth:
            return None

        try:
            token = auth[0].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)
        except IndexError:
            msg = _('로그인되지 않았습니다.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)
