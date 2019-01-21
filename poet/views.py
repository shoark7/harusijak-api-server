from django.contrib.auth import authenticate
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from .models import Poet
from .serializers import PoetCreateSerializer, PoetSerializer
from .permissons import IsOneselfOrReadOnly


class PoetList(APIView):
    queryset = Poet.objects.all()
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        poets = Poet.objects.all()
        serializer_context = {
            'request': request,
        }
        serializer = PoetSerializer(poets, context=serializer_context, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if request.data.get('password') != request.data.get('password_conf'):
            return Response({'error': '비밀번호가 일치하지 않습니다.'},
                            status=HTTP_400_BAD_REQUEST)

        serializer = PoetCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PoetDetail(APIView):
    queryset = Poet.objects.all()
    permission_classes = (IsOneselfOrReadOnly,)

    def get_object(self, pk):
        try:
            return Poet.objects.get(pk=pk)
        except Poet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        poet = self.get_object(pk)
        serializer_context = {
            'request': request,
        }
        serializer = PoetSerializer(poet, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        poet = self.get_object(pk)
        self.check_object_permissions(request, poet)
        serializer_context = {'request': request}
        serializer = PoetSerializer(poet, context=serializer_context, data=request.data)

        if serializer.is_valid():
            serializer.save()
            poet.set_password(serializer.data['password'])
            poet.save()
            return Response({
                             'pk': poet.pk,
                             'identifier': poet.identifier,
                             'nickname': poet.nickname,
                             'image': poet.image or None,
                             'description': poet.description or '',
                            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        poet = self.get_object(pk)
        self.check_object_permissions(request, poet)
        poet.delete()
        return Response({"message": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
