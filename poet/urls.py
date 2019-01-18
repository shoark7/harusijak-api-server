from django.urls import include, path

from . import views


app_name = 'poet'
urlpatterns = [
    path('', views.PoetList.as_view(), name='list'),
    path('<int:pk>/', views.PoetDetail.as_view(), name='detail',),
]
