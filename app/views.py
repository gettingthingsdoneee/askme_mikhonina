from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import copy
from django.core.paginator import Paginator
from app.models import Question, Answer
from app.forms import LoginForm, ProfileForm, QuestionForm, AnswerForm

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
    form = AnswerForm()
    answers = Answer.objects.hot_answers()

    page, page_range = paginate(answers, request, 3)
    return render(request, 'single_question.html', context={'question': Question.objects.questions_in_order()[question_id-1], 'answers': page.object_list, 'page_obj' : page, 'page_range' : page_range, 'form':form}  )

def tag(request, tag): 
    questions = Question.objects.questions_by_tag(tag)
    return render(request, 'index.html', context={'questions': questions})



def login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                # redirect_to = request.GET.get('continue', '') or reverse('profile')
                # return redirect(request.GET.get('continue', 'profile'))
                # return redirect(redirect_to)
                return redirect(f"{reverse('login')}?continue=/profile/{user.username}/")
            else:
                form.add_error(None, error="User not found")
    return render(request, 'login.html', context={'form': form})

def signup(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    return render(request, 'signup.html', context={'form': form})

def ask(request):
    form = QuestionForm()
    return render(request, 'ask.html', context={'form': form})

def logout(request):
    auth.logout(request)
    return redirect('.')

@login_required(login_url=reverse_lazy('login'))
def profile(request):
    return render(request, 'profile.html')

