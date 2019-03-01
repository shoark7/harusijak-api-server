from rest_framework.authentication import get_authorization_header, TokenAuthentication


class CustomTokenAuthentication(TokenAuthentication):
    keyword = ''

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        try:
            token = auth[0].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)
