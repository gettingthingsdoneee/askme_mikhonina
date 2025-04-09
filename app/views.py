from django.shortcuts import render
from django.core.paginator import Paginator
import copy
from app.models import Question, Profile

QUESTIONS = [
    {
    'title' : f'Title {i}',
    'id' : i,
    'text' : f'This is text for question # {i}'
 } for i in range (1,30)
]

ANSWERS = [
    {
    'title' : f'Answer {i}',
    'id' : i,
    'text' : f'This is text for answer # {i}'
 } for i in range (1,4)
]





def index(request):
    page_num = int(request.GET.get('page',1 ))
    paginator = Paginator(QUESTIONS, per_page= 5)
    page = paginator.page(page_num)
    questions = Question.objects.new_questions()
    return render(request, 'index.html', context={'questions': questions, 'page_obj' : page})

def hot(request):
    page_num = int(request.GET.get('page',1 ))
    paginator = Paginator(QUESTIONS, per_page= 5)
    page = paginator.page(page_num)
    questions = Question.objects.hot_questions()
    return render(request, 'hot.html', context={'questions': questions, 'page_obj' : page})

def tag(request):
    questions = Question.objects.questions_by_tag('django')
    return render(request, 'index.html', context={'questions': questions})

def question(request, question_id):
    return render(request, 'single_question.html', context={'question': QUESTIONS[question_id], 'answers': ANSWERS})

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'ask.html')

def profile(request):
    return render(request, 'profile.html')

