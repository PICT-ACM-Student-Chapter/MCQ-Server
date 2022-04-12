from django.urls import path

from . import views

urlpatterns = [
    path('user/event/list', views.UserEventListView.as_view(), name='list_user_event'),
    path('user/event/get', views.UserEventListView.as_view(), name='get_user_event'),
]