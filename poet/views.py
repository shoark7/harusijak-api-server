from django.contrib.auth import authenticate, logout, login
from django.shortcuts import redirect, render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Poet
from .serializers import PoetSerializer, PoetCreateSerializer


class PoetList(APIView):
    """
    List all poets, or create a new poet.
    """
    queryset = Poet.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        poets = Poet.objects.all()
        serializer_context = {
            'request': request,
        }
        serializer = PoetSerializer(poets, context=serializer_context, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if request.data['password'] != request.data['password_conf']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        request.data.pop('password_conf')

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
        serializer_context = {
            'request': request,
        }
        serializer = PoetSerializer(poet, context=serializer_context, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        poet = self.get_object(pk)
        poet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)













def log_out(request):
    logout(request)
    return redirect('index')


def log_in(request):
    if request.method == 'GET':
        form = PoetLoginForm()
    else:
        identifier = request.POST['identifier']
        password = request.POST['password']

        poet = authenticate(request, identifier=identifier, password=password)
        if poet is not None:
            login(request, poet)
            return redirect('index')
        else:
            form = PoetLoginForm(request.POST)
            """로그인 실패시 데이터 출력이 필요"""
    return render(request, 'poet/poet_login.html', {'form': form})


def sign_in(request):
    if request.method == 'GET':
        form = PoetCreationForm()
    else:
        form = PoetCreationForm(request.POST, request.FILES)
        if form.is_valid():
            poet = form.save()
            login(request, poet)
            return redirect('index')
    return render(request, 'poet/poet_signin.html', {'form': form})


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
