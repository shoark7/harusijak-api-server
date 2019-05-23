from django.urls import include, path

from rest_framework import routers, serializers

from . import views
from poem.models import Poem
from poet.models import Poet


urlpatterns = [
    path('', views.PoemList.as_view()),
    path('about-today/', views.about_today, name='about-today'),
    path('search/', views.PeomSearch.as_view(), name='poem-search'),
    path('<str:pk>/', views.PoemDetail.as_view(), name='poem-detail',),
    path('<str:pk>/like/', views.toggle_like, name='toggle-like',),
    path('<str:pk>/dislike/', views.toggle_dislike, name='toggle-dislike',),
]
