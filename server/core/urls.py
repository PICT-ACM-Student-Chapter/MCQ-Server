from django.urls import path

from . import views

urlpatterns = [
    path('event/list', views.UserEventListView.as_view(), name='list_user_event'),
    path('event/get/<uuid:id>', views.UserEventGetView.as_view(), name='get_user_event'),
    path('question/answer', views.UserQuestionAnswer.as_view(), name='answer_user_question'),
    path('question/list/<uuid:id>', views.UserQuestionListView.as_view(), name='list_user_question'),
    path('event/submit/<uuid:id>', views.UserSubmitEventView.as_view(), name='submit_user_event'),
]