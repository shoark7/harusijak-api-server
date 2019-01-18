
from django.urls import include, path

from . import views


urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
]
