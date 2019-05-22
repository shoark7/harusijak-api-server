from django.urls import include, path

from . import views


urlpatterns = [
    path('current-user/', views.current_user, name='current-user'),
    path('', views.PoetList.as_view(), name='poet-list'),
    path('<int:pk>/', views.PoetDetail.as_view(), name='poet-detail',),
    path('<int:pk>/poems/', views.Poems_of.as_view(), name='poems_of_user_id',),
    path('<int:pk>/subscribing/', views.PoetsSubscribing.as_view(), name='poets_subscribing',),
    path('<int:pk>/subscribe/', views.toggle_subscribe, name='subscribe_poet',),
    path('<int:pk>/subscribed_by/', views.PoetsSubscribedBy.as_view(), name='poets_subscribed_by',),
]
