import os
from datetime import datetime, timezone
import requests
import random
import json

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model

from drf_yasg.utils import swagger_auto_schema

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserEventSerializer, UserEventListSerializer, UserQuestionAnswerSerializer, UserQuestionRequestSerializer, UserQuestionGetSerializer, LoginSerializer, EventListSerializer, QuestionSerializer
from .models import Event, Question, User_Event, User_Question, User_Token
from .tasks import process_result
# Create your views here.

User = get_user_model()

class LoginView(APIView):
    """LOGIN API VIEW THAT ACCEPTS EMAIL
    AND PASSWORD AND RETURNS A TOKEN"""
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(data={'error': 'invalid data'},
                            status=status.HTTP_400_BAD_REQUEST)            

        url = '{}/user/signin'.format(os.environ.get('EMS_API'))
        data = {
            'email': email,
            'password': password
        }
        res = requests.post(url, data=data, verify=False)
        if res.status_code == status.HTTP_401_UNAUTHORIZED:
            return Response(data=res.json(),
                            status=status.HTTP_401_UNAUTHORIZED)

        # get user
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            user = User.objects.create_user(username=email,
                                            email=email, password=password)
            user.first_name = res.json().get('user').get('first_name')
            user.last_name = res.json().get('user').get('last_name')
            user.save()
        # Create user_token object for future use
        User_Token.objects.create(fk_user=user, token=res.json().get('token'))

        if res.status_code == status.HTTP_200_OK:
            token = res.json().get('token')
            # query my events
            url = '{}/user_events'.format(os.environ.get('EMS_API'))
            myevent_res = requests.get(url, headers={
                'Authorization': 'Bearer ' + token}, verify=False)

            if myevent_res.status_code == status.HTTP_401_UNAUTHORIZED:
                return Response(data=myevent_res.json(),
                                status=status.HTTP_401_UNAUTHORIZED)

            events = myevent_res.json().get('events')
            for event in events:
                try:
                    slot_id = event.get('fk_slot')
                except TypeError:
                    slot_id = None

                if slot_id:
                    try:
                        event = Event.objects.get(ems_slot_id=slot_id)
                        # create user contest
                        ue, _ = User_Event.objects.get_or_create(
                        fk_user=user, fk_event=event)
                    except Event.DoesNotExist:
                        continue

            # create jwt token
            refresh = RefreshToken.for_user(user)

            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data=data, status=status.HTTP_200_OK)


class UserEventListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    """API VIEW THAT RETURNS USER ALL USER EVENTS"""
    @swagger_auto_schema(
        operation_description="Returns user events",
        responses={
            200: UserEventListSerializer(many=True)
        }
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        user_events = User_Event.objects.filter(fk_user=user)
        for user_event in user_events:
            if user_event.fk_event.start_time <= datetime.now().replace(tzinfo=timezone.utc) <= user_event.fk_event.end_time:
                user_event.started = True
            if user_event.fk_event.end_time < datetime.now().replace(tzinfo=timezone.utc):
                user_event.finished = True

            user_event.save()
        serializer = UserEventListSerializer(user_events, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserEventGetView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    """API VIEW THAT RETURNS USER EVENT BY ID"""
    @swagger_auto_schema(
        operation_description="Returns user event by id",
        responses={
            200: UserEventSerializer()
        }
    )
    def get(self, request, id):
        user = request.user
        try:
            user_event = User_Event.objects.get(fk_user=user, id=id, started=True, finished=False)
            if user_event.fk_event.end_time < datetime.now().replace(tzinfo=timezone.utc):
                return Response(data={'error': 'event finished'},
                                status=status.HTTP_404_NOT_FOUND)

        except User_Event.DoesNotExist:
            return Response(data={'error': 'event finished or not started yet'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = UserEventSerializer(instance=user_event)   
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserQuestionAnswer(APIView):
    permission_classes = [permissions.IsAuthenticated]
    """API VIEW FOR POST REQUEST OF ANSWER MARKING/MARKING FOR REVIEW"""
    @swagger_auto_schema(request_body=UserQuestionAnswerSerializer,
                         responses={200: UserQuestionAnswerSerializer})
    def patch(self, request, *args, **kwargs):
        user_question = User_Question.objects.get(id=request.data['id'])
        serializer = UserQuestionAnswerSerializer(user_question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserQuestionListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    """API VIEW THAT RETURNS USER QUESTIONS"""
    @swagger_auto_schema(
        operation_description="Returns user questions",
        responses={
            200: UserQuestionGetSerializer(many=True)
        }
    )
    def get(self, request, id, *args, **kwargs):
        user = request.user
        user_questions = User_Question.objects.filter(fk_user=user, 
                                                    fk_question__fk_event=id)
        if user_questions:
            user_question = user_questions[0]
            if user_question.fk_question.fk_event.end_time < datetime.now().replace(tzinfo=timezone.utc):
                return Response(data={'error': 'event finished'},
                                status=status.HTTP_404_NOT_FOUND)

            elif user_question.fk_question.fk_event.start_time > datetime.now().replace(tzinfo=timezone.utc):
                return Response(data={'error': 'event not started yet'},
                                status=status.HTTP_404_NOT_FOUND)
            elif user_question.fk_question.fk_event.user_event_set.filter(fk_user=user, started=True, finished=True).exists():
                return Response(data={'error': 'event submitted already'},
                                status=status.HTTP_404_NOT_FOUND)

            serializer = UserQuestionGetSerializer(user_questions, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            questions = list(Question.objects.filter(fk_event=id))
            if questions:
                random_questions = random.sample(questions, min(questions[0].fk_event.no_of_questions, len(questions)))
                for question in random_questions:
                    User_Question.objects.create(fk_user=user, fk_question=question)

            user_questions = User_Question.objects.filter(fk_user=user,
                                                        fk_question__fk_event__id=id) 
            if user_questions:
                serializer = UserQuestionGetSerializer(user_questions, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserSubmitEventView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    """API VIEW THAT STARTS SUBMISSIONS PROCESS"""
    def get(self, request, id, *args, **kwargs):
        user = request.user
        user_event = User_Event.objects.get(id=id)
        if user_event.fk_user == user:
            user_event.finished = True
            user_event.save()
            _ = process_result.apply_async(kwargs={"user_event_id": user_event.id})
            return Response(data={"success":"Test submitted successfully!"}, status=status.HTTP_200_OK)

        return Response(data={"error": "User not authorised"}, status=status.HTTP_403_FORBIDDEN)