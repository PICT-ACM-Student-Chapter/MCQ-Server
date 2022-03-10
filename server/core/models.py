from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model

import uuid

# Create your models here.
class Event(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=50)
    ems_event_id = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    statement = models.TextField()
    options = ArrayField(models.TextField(), size=4)
    correct_option = models.PositiveIntegerField()
    fk_event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User_Question(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    fk_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    fk_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    answer = models.PositiveIntegerField()
    review_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User_Result(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    fk_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    fk_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User_Token(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    fk_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)