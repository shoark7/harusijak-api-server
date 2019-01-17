from django.contrib.auth import authenticate, logout, login
from django.shortcuts import redirect, render

from .forms import PoetLoginForm, PoetCreationForm


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
