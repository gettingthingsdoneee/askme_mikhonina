from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('-created_at')

    def hot_questions(self):
        return self.order_by('likes')

    def questions_by_tag(self, tag):
        return self.filter(tags__name='tag')



class Question(models.Model):
    objects = QuestionManager
    name = models.CharField(max_length=255)
    text = models.TextField
    tag = models.ManyToManyField('Tag')
    created_at = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey('Profile', on_delete=models.PROTECT)
    likes = models.ForeignKey('QuestionLikes', on_delete=models.PROTECT)

    def __str__(self):
        return self.name

class Answer(models.Model):
    text = models.TextField
    profile = models.ForeignKey('Profile', on_delete=models.PROTECT)
    question = models.ForeignKey('Question', on_delete=models.PROTECT)
    correct = models.BooleanField
    likes = models.ForeignKey('AnswerLkes', on_delete=models.PROTECT)


class Tag(models.Model):
    name = models.CharField(max_length=255)

class AnswerLike(models.Model):
    count = models.PositiveIntegerField(default=0)
    unique_together= ["AnswerLike", "Profile"]

class QuestionLike(models.Model):
    count  = models.PositiveIntegerField(default=0)
    unique_together= ["QuestionLike", "Profile"]
    

class Profile(models.Model):
    nickname = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='user.jpg')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
