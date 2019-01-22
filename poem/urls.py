from django.urls import include, path

from rest_framework import routers, serializers

from . import views
from poem.models import Poem
from poet.models import Poet


urlpatterns = [
    path('', views.PoemList.as_view()),
    path('<str:pk>/', views.PoemDetail.as_view(), name='poem-detail',),
]
