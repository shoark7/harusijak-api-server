from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    identifier = request.data.get("identifier")
    password = request.data.get("password")
    if identifier is None or password is None:
        return Response({'error': 'Please provide both identifier and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(identifier=identifier, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key,
                     'pk': user.pk,
                     'identifier': user.identifier,
                     'nickname': user.nickname,
                     'image': user.image or None,
                     'description': user.description or '',
                    },
                    status=HTTP_200_OK)


@api_view(["GET"])
def logout(request):
    request.user.auth_token.delete()
    return Response({'message': 'Successfully logged out'}, status=HTTP_200_OK)
