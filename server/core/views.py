import os
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import *
from .models import Event, User_Event
# Create your views here.

User = get_user_model()

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(data={'error': 'invalid data'},
                            status=status.HTTP_400_BAD_REQUEST)

        # TODO: CHECK EMS API CALL AND RESPONSE
        url = '{}/auth/login'.format(os.environ.get('EMS_API'))
        data = {
            'email': email,
            'password': password
        }
        res = requests.post(url, data=data)

        if res.status_code == status.HTTP_401_UNAUTHORIZED:
            return Response(data=res.json(),
                            status=status.HTTP_401_UNAUTHORIZED)

        # get user
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            user = User.objects.create_user(username=email,
                                            email=email, password=password)
            user.first_name = res.json().get('user').get('fname')
            user.last_name = res.json().get('user').get('lname')
            user.save()

        if res.status_code == status.HTTP_200_OK:
            token = res.json().get('token')
            # query my events
            # TODO: CHECK EMS API CALL AND RESPONSE FOR SLOTS AND EVENTS
            url = '{}/myevents'.format(os.environ.get('EMS_API'))
            myevent_res = requests.get(url, headers={
                'Authorization': 'Bearer ' + token})

            if myevent_res.status_code == status.HTTP_401_UNAUTHORIZED:
                return Response(data=myevent_res.json(),
                                status=status.HTTP_401_UNAUTHORIZED)

            events = myevent_res.json()

            for event in events:
                try:
                    # TODO: CHECK JSON FOR EVENT RESPONSE
                    slot_id = event['slot_id']['_id']
                except TypeError:
                    slot_id = None

                if slot_id:
                    try:
                        event = Event.objects.get(ems_slot_id=slot_id)
                    except Event.DoesNotExist:
                        continue

                    # create user contest
                    ue, _ = User_Event.objects.get_or_create(
                        fk_user=user, fk_event=event)

            # create jwt token
            refresh = RefreshToken.for_user(user)

            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data=data, status=status.HTTP_200_OK)