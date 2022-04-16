from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from martor.models import MartorField

import uuid

class User(AbstractUser):
    current_user_event = models.UUIDField(null=True)

# Create your models here.
# TODO: IMAGE FOR EVENT
class Event(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=50)
    image_url = models.URLField(null=False)
    ems_event_id = models.CharField(max_length=100)
    ems_slot_id = models.CharField(max_length=100, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    no_of_questions = models.PositiveIntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# TODO: ADD IMAGE AND CODE FIELDS
class Question(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    statement = models.TextField()
    options = ArrayField(models.TextField(), size=4)
    code = models.TextField(null=True, blank=True)
    correct_option = models.PositiveIntegerField()
    fk_event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User_Question(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    fk_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    fk_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    answer = models.PositiveIntegerField(null=True)
    review_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User_Event(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    fk_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    fk_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    started = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class User_Result(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    fk_user_event = models.ForeignKey(User_Event, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User_Token(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    fk_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=500)
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
