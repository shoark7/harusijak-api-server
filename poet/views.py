from django.contrib.auth import authenticate
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404

from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from .models import Poet
from .serializers import PoetSerializer, PoetCreateSerializer


class PoetList(APIView):
    """
    List all poets, or create a new poet.
    """
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
        if request.data['password'] != request.data['password_conf']:
            return Response({'error': '비밀번호가 일치하지 않습니다.'},
                            status=HTTP_400_BAD_REQUEST)

        serializer = PoetCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PoetDetail(APIView):
    queryset = Poet.objects.all()

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
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        poet = self.get_object(pk)
        if poet != request.user:
            return Response({'error': '본인이 아닙니다.'},
                            status=HTTP_404_NOT_FOUND)
        serializer_context = {
            'request': request,
        }

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        poet = self.get_object(pk)
        if poet != request.user:
            return Response({'error': '본인이 아닙니다.'},
                            status=HTTP_400_BAD_REQUEST)
        poet.delete()
        return Response({"message": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


# class AuthView(APIView):
    # queryset = Poet.objects.all()

    # def post(self, request, format=None):
        # try:
            # identifier = request.POST['identifier']
            # password = request.POST['password']
        # except:
            # raise serializer.ValidationError("아이디와 비밀번호를 입력하세요.")

        # poet = authenticate(request, identifier=identifier, password=password)
        # poet.save()
        # if poet is not None:
            # return Response(poet.token, status=status.HTTP_204_NO_CONTENT)
        # else:
            # raise serializer.ValidationError("정보가 없습니다.")



# def log_in(request):
    # if request.method == 'GET':
        # form = PoetLoginForm()
    # else:
        # identifier = request.POST['identifier']
        # password = request.POST['password']

        # poet = authenticate(request, identifier=identifier, password=password)
        # if poet is not None:
            # login(request, poet)
            # return redirect('index')
        # else:
            # form = PoetLoginForm(request.POST)
            # """로그인 실패시 데이터 출력이 필요"""
    # return render(request, 'poet/poet_login.html', {'form': form})


# def sign_in(request):
    # if request.method == 'GET':
        # form = PoetCreationForm()
    # else:
        # form = PoetCreationForm(request.POST, request.FILES)
        # if form.is_valid():
            # poet = form.save()
            # login(request, poet)
            # return redirect('index')
    # return render(request, 'poet/poet_signin.html', {'form': form})


"""
def update(request):
    if request.method == 'GET':
        form = PoetCreationForm(instance=request.user)
    else:
        form = PoetCreationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            poet = form.save()
            login(request, poet)
            return redirect('index')
    return render(request, 'poet/poet_signin.html', {'form': form})
"""
