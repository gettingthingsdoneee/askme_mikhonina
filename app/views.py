from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import copy
from django.core.paginator import Paginator
from app.models import Question, Answer, Profile, QuestionLike, AnswerLike
from app.forms import LoginForm, ProfileForm, QuestionForm, AnswerForm
from django.db.models import Count
from django.shortcuts import get_object_or_404

def paginate(objects_list, request, per_page=5):
    page_num = int(request.GET.get('page',1 ))
    paginator = Paginator(objects_list, per_page)
    page = paginator.page(page_num)
    page_range = paginator.get_elided_page_range(page_num, on_each_side=1, on_ends=1)
    return page, page_range

def get_user_profile(request):
    if request.user.is_authenticated:
        profile, _ = Profile.objects.get_or_create(user = request.user)
        return profile
    return None


def index(request):
    questions = Question.objects.new_questions()
    profile = get_user_profile(request)
    page, page_range = paginate(questions, request, 5)
    return render(request, template_name='index.html', context={'questions': page.object_list, 'page_obj' : page, 'page_range' : page_range, 'profile': profile})
    

def hot(request):
    questions = Question.objects.hot_questions()
    profile = get_user_profile(request)
    page, page_range = paginate(questions, request, 5)
    return render(request, template_name='hot.html', context={'questions': page.object_list, 'page_obj' : page, 'page_range' : page_range, 'profile': profile})

def question(request, question_id):
    form = AnswerForm()
    answers = Answer.objects.new_answers()
    profile = get_user_profile(request)
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.profile = profile
            answer.question = Question.objects.questions_in_order()[question_id-1]
            answer.text 
            answer.save()
            return redirect('question', question_id=question_id)

    page, page_range = paginate(answers, request, 3)
    return render(request, 'single_question.html', context={'question': Question.objects.questions_in_order()[question_id-1], 'answers': page.object_list, 'page_obj' : page, 'page_range' : page_range, 'form':form, 'profile':profile}  )

def tag(request, tag): 
    questions = Question.objects.questions_by_tag(tag)
    profile = get_user_profile(request)
    return render(request, 'index.html', context={'questions': questions, 'profile': profile})



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

@login_required(login_url=reverse_lazy('login'))
def ask(request):
    form = QuestionForm()
    profile = get_user_profile(request)
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.profile = profile
            question.save()
            return redirect('.')
    return render(request, 'ask.html', context={'form': form, 'profile': profile})

    

def logout(request):
    auth.logout(request)
    return redirect('.')

from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile,
            user=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = ProfileEditForm(
            instance=request.user.profile,
            user=request.user
        )
    return render(request, 'profile_edit.html', {'form': form})

@login_required()
def question_like(request, question_id):
    profile = get_user_profile(request)
    question = get_object_or_404(Question, id=question_id)
    question_like, is_created = QuestionLike.objects.get_or_create(question=question, profile=profile)
    if is_created is False:
        question_like.delete()
    question.likes_count = QuestionLike.objects.filter(question=question).count()
    question.save()    
    return redirect('question', question_id=question_id)  

@login_required()
def answer_like(request, answer_id):
    profile = get_user_profile(request)
    answer = get_object_or_404(Answer, id=answer_id)
    question_id = answer.question.id
    answer_like, is_created = AnswerLike.objects.get_or_create(answer=answer, profile=profile)
    if is_created is False:
        answer_like.delete()
    answer.likes_count = AnswerLike.objects.filter(answer=answer).count()
    answer.save()    
    return redirect('question', question_id=question_id)  

@login_required()
def correct_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    question_id = answer.question.id
    answer.correct = not answer.correct   
    answer.save()    
    return redirect('question', question_id=question_id)