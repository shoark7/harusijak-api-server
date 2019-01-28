from django.urls import include, path

from . import views


urlpatterns = [
    path('login/', views.login, name='login',),
    path('logout/', views.logout, name='logout',),
]
