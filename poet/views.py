from django.contrib.auth import authenticate
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404

from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.views import APIView

from .models import Poet
from .permissons import IsOneself, IsOneselfOrReadOnly
from .serializers import PoetCreateSerializer, PoetSerializer


class PoetList(APIView):
    queryset = Poet.objects.all()
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        poets = Poet.objects.all()
        serializer_context = {'request': request}
        serializer = PoetSerializer(poets, context=serializer_context, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # serializer = PoetCreateSerializer(data=request.data)
        serializer = PoetSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key,
                             'pk': user.pk,
                             'identifier': user.identifier,
                             'nickname': user.nickname,
                             'image': user.image.url if user.image else None,
                             'description': user.description or None
                            },
                            status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PoetDetail(APIView):
    queryset = Poet.objects.all()
    permission_classes = (IsOneself,)

    def get_object(self, pk):
        try:
            return Poet.objects.get(pk=pk)
        except Poet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        poet = self.get_object(pk)
        serializer_context = {'request': request}
        serializer = PoetSerializer(poet, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        poet = self.get_object(pk)
        self.check_object_permissions(request, poet)
        serializer_context = {'request': request}
        serializer = PoetSerializer(poet, context={'request': request}, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            # 비밀번호 변경 시의 로직은 따로 구현하거나 해야 할듯.
            if hasattr(serializer.data, 'password'):
                poet.set_password(serializer.data['password'])
                poet.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        poet = self.get_object(pk)
        self.check_object_permissions(request, poet)
        poet.delete()
        return Response({"message": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)



@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def current_user(request):
    user = request.user
    if not request.user.is_authenticated:
        raise serializers.ValidationError("로그인해야 합니다")
    return Response({
                     'pk': user.pk,
                     'identifier': user.identifier,
                     'nickname': user.nickname,
                     'image': user.image.url if user.image else None,
                     'description': user.description or '',
                    },
                    status=HTTP_200_OK)
