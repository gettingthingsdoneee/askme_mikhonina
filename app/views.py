#from django.http import HttpResponse
from django.shortcuts import render

QUESTIONS = [
    {
    'title' : f'Title {i}',
    'id' : i,
    'text' : f'This is text for question # {i}'
 } for i in range (30)
]

# Create your views here.

def index(request):
    #return HttpResponse('Hello World')
    return render(request, 'index.html', context={'questions': QUESTIONS})
