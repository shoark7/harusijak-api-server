from django.urls import include, path

from . import views


app_name = 'poet'
urlpatterns = [
    path('', views.PoetList.as_view(), name='list'),
    path('<int:pk>/', views.PoetDetail.as_view(), name='detail',),
    # path('signin/', views.sign_in, name='signin'),
    # path('logout/', views.log_out, name='logout'),
    # path('login/', views.log_in, name='login'),
    # path('update/', views.update, name='update'),
]
