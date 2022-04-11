from rest_framework import serializers

from .models import User_Event, Event


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'start_time', 'end_time', 'ems_event_id', 'ems_slot_id', ]

class UserEventListSerializer(serializers.ModelSerializer):
    fk_event = EventListSerializer()

    class Meta:
        model = User_Event
        fields = ['id', 'fk_event', 'started']


class UserEventSerializer(serializers.ModelSerializer):
    fk_event = EventListSerializer()

    class Meta:
        model = User_Event
        fields = [id, 'fk_event', 'started', 'finished', ]