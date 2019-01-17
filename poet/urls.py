from django.urls import include, path

from . import views


app_name = 'poet'
urlpatterns = [
    path('signin/', views.sign_in, name='signin'),
    path('logout/', views.log_out, name='logout'),
    path('login/', views.log_in, name='login'),
    # path('update/', views.update, name='update'),
]
