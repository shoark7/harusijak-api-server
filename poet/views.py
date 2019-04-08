from django.contrib.auth import authenticate
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404

from rest_framework import generics, mixins, serializers, status
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
from .permissons import IsOneself, IsOneselfOrReadOnly, ReadOnly
from .serializers import PoetSerializer
from poem.models import Poem
from poem.serializers import PoemSerializer


class PoetList(APIView):
    queryset = Poet.objects.all()
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        poets = Poet.objects.all()
        serializer = PoetSerializer(poets, context={'request': request}, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PoetSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(user.password)
            user.save()
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
    permission_classes = (IsOneselfOrReadOnly,)

    def get_object(self, pk):
        try:
            poet = Poet.objects.get(pk=pk)
        except Poet.DoesNotExist:
            raise Http404
        else:
            self.check_object_permissions(self.request, poet)
            return poet

    def get(self, request, pk, format=None):
        poet = self.get_object(pk)
        serializer = PoetSerializer(poet, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        poet = self.get_object(pk)
        self.check_object_permissions(request, poet)
        serializer = PoetSerializer(poet, context={'request': request}, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            if 'password' in serializer.data:
                poet.set_password(serializer.data['password'])
                poet.save()
                serializer = PoetSerializer(poet, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        poet = self.get_object(pk)
        self.check_object_permissions(request, poet)
        poet.delete()
        return Response({"message": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


# @api_view(["GET"])
# @permission_classes((ReadOnly,))
# def poems_of(request, pk):
    # poems = Poem.objects.filter(writer=pk)
    # serializer = PoemSerializer(poems, context={'request': request}, many=True)
    # return Response(serializer.data, status=status.HTTP_200_OK)


class Poems_of(mixins.ListModelMixin,
               generics.GenericAPIView):
    # queryset = Poem.objects.all()
    serializer_class = PoemSerializer
    permission_classes = (ReadOnly,)

    def get_queryset(self, pk):
        poet = get_object_or_404(Poet, pk=pk)
        return poet.poems.all()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(kwargs['pk']))
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data) if page else Response(serializer.data)


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def current_user(request):
    user = request.user
    return Response({
                     'pk': user.pk,
                     'identifier': user.identifier,
                     'nickname': user.nickname,
                     'image': user.image.url if user.image else None,
                     'description': user.description or '',
                    },
                    status=HTTP_200_OK)
