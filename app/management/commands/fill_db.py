from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, QuestionLike, AnswerLike, Tag
from django.utils.crypto import get_random_string

class Command (BaseCommand):
    help = 'Fills the database'

    def add_arguments(self, parser):
        return parser.add_argument('ratio', type=int)
    
    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        user_instances =[User(username=get_random_string(10), email='hello@hi.com', password='password') for i in range(ratio)]
        User.objects.bulk_create(user_instances)

        #last_user = User.objects.order_by('-pk').first()
        #user_id = last_user.pk - ratio + 1 

        profile_instances =[Profile(user=user, avatar='avatars/bird.jpg', nickname=get_random_string(9)) for user in user_instances]
        Profile.objects.bulk_create(profile_instances) 

        tag_instances =[Tag(name=get_random_string(10)) for i in range(ratio)]
        Tag.objects.bulk_create(tag_instances) 

        #last_tag = Tag.objects.order_by('-pk').first()
        #tag_id = last_tag.pk - ratio + 1

        question_instances =[Question(profile=profile_instances[i%len(profile_instances)], name=get_random_string(18), text='blabla' ) for i in range(ratio*10)]
        Question.objects.bulk_create(question_instances) 

        for i, question in enumerate(question_instances):
            question.tag.add(tag_instances[i % len(tag_instances)])
            
        #last_question = Question.objects.order_by('-pk').first()
        #question_id = last_question.pk - ratio + 1

        answer_instances =[Answer(profile=profile_instances[i%len(profile_instances)], text='blabla', question=question_instances[(i+j)%len(question_instances)]) for i in range(ratio*10) for j in range(10)]
        Answer.objects.bulk_create(answer_instances) 

        questionlike_instances =[QuestionLike(profile=profile_instances[i%len(profile_instances)], question=question_instances[(i+j)%len(question_instances)]) for i in range(ratio*10) for j in range(10)]
        QuestionLike.objects.bulk_create(questionlike_instances) 

        #last_answer = Answer.objects.order_by('-pk').first()
        #answer_id = last_answer.pk - ratio + 1

        answerlike_instances =[AnswerLike(profile=profile_instances[i%len(profile_instances)], answer=(answer_instances[(i+j)%len(answer_instances)])) for i in range(ratio*10) for j in range(10) ]
        AnswerLike.objects.bulk_create(answerlike_instances) 
        