from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class QuestionManager(models.Manager):
    def questions_in_order(self):
        return self.order_by('created_at')
    
    def new_questions(self):
        return self.order_by('-created_at')

    def hot_questions(self):
        return self.order_by('likes_count')

    def questions_by_tag(self, tag):
        return self.filter(tags__name=tag)
    
class AnswerManager(models.Manager):
    def hot_answers(self):
        return self.order_by('likes_count')   

class Question(models.Model):
    objects = QuestionManager()
    name = models.CharField(max_length=255)
    text = models.TextField(default='')
    tag = models.ManyToManyField('Tag')
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey('Profile', on_delete=models.PROTECT)
    likes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Answer(models.Model):
    objects = AnswerManager()
    text = models.TextField(default='')
    profile = models.ForeignKey('Profile', on_delete=models.PROTECT)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    likes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.text


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AnswerLike(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    answer = models.ForeignKey('Answer', on_delete=models.CASCADE)
    class Meta:
        unique_together= ["answer", "profile"]

    def __str__(self):
        return f"Like #{self.id} on Answer #{self.answer.id}"

class QuestionLike(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    class Meta:
        unique_together= ["question", "profile"]

    def __str__(self):
        return f"Like #{self.id} on Question #{self.question.id}"
    

class Profile(models.Model):
    nickname = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname
