from django.urls import include, path

from rest_framework import routers, serializers, viewsets

from . import views
from poet.models import Poet
from poem.models import Poem


urlpatterns = [
    path('', views.PoemList.as_view()),
    path('<str:pk>/', views.PoemDetail.as_view(), name='poem-detail',),
]
