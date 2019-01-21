from django.urls import include, path

from . import views


urlpatterns = [
    path('', views.PoetList.as_view(), name='poet-list'),
    path('<int:pk>/', views.PoetDetail.as_view(), name='poet-detail',),
]
