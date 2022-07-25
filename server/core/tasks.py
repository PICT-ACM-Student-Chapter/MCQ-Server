from celery import shared_task
from .models import User_Event, User_Question, User_Result


@shared_task
def process_result(**kwargs):
    score = 0
    user_event = User_Event.objects.get(id=kwargs.get('user_event_id'))
    user = user_event.fk_user
    user_result = User_Result.objects.create(score=0, fk_user_event=user_event)
    user_questions = User_Question.objects.filter(fk_user=user, fk_question__fk_event=user_event.fk_event)
    for user_question in user_questions:
        if user_question.fk_question.correct_option == user_question.answer:
            score += 1

    user_result.score = score
    user_result.save()
    return

@shared_task
def process_new_result(**kwargs):
    user_events = User_Event.objects.all()
    for user_event in user_events:
        score = 0
        user = user_event.fk_user
        user_result = User_Result.objects.create(score=0, fk_user_event=user_event)
        user_questions = User_Question.objects.filter(fk_user=user, fk_question__fk_event=user_event.fk_event)
        for user_question in user_questions:
            if user.fk_question.correct_option == user_question.answer:
                score += 1
        user_result.score = score
        user_result.save()
    
    return 
