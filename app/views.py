from django.shortcuts import render
import copy
from django.core.paginator import Paginator
from app.models import Question, Answer

def paginate(objects_list, request, per_page=5):
    page_num = int(request.GET.get('page',1 ))
    paginator = Paginator(objects_list, per_page)
    page = paginator.page(page_num)
    page_range = paginator.get_elided_page_range(page_num, on_each_side=1, on_ends=1)
    return page, page_range


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
 } for i in range (1,15)
]

def index(request):
    questions = Question.objects.new_questions()
    page, page_range = paginate(questions, request, 5)
    return render(request, template_name='index.html', context={'questions': page.object_list, 'page_obj' : page, 'page_range' : page_range})
    

def hot(request):
    questions = Question.objects.hot_questions()
    page, page_range = paginate(questions, request, 5)
    return render(request, template_name='hot.html', context={'questions': page.object_list, 'page_obj' : page, 'page_range' : page_range})

def question(request, question_id):
    answers = Answer.objects.hot_answers()

    page, page_range = paginate(answers, request, 3)
    return render(request, 'single_question.html', context={'question': Question.objects.questions_in_order()[question_id-1], 'answers': page.object_list, 'page_obj' : page, 'page_range' : page_range})

def tag(request, tag): 
    questions = Question.objects.questions_by_tag(tag)
    return render(request, 'index.html', context={'questions': questions})


def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def ask(request):
    return render(request, 'ask.html')

def profile(request):
    return render(request, 'profile.html')