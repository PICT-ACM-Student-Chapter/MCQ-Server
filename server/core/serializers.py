from rest_framework import serializers

from .models import Question, User_Event, Event, User_Question


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
    fk_event = EventListSerializer(many=False)

    class Meta:
        model = User_Event
        fields = ['id', 'fk_event', 'started', 'finished']


class UserQuestionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Question
        fields = ['id', 'fk_question', 'answer', 'review_status']


class QuestionSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Question
        fields = ['id', 'statement', 'options', 'fk_event']

class UserQuestionGetSerializer(serializers.ModelSerializer):
    fk_question = QuestionSerializer()

    class Meta: 
        model = User_Question
        fields = ['id', 'fk_question', 'answer', 'review_status']


class UserQuestionAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User_Question
        fields = ['id', 'fk_question', 'answer', 'review_status']
