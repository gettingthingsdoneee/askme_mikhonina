from app import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('hot', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='question'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('ask', views.ask, name='ask'),
    path('tag/<str:tag>', views.tag, name='tag/blabla'), #/tag_name
    path('profile', views.profile, name='profile'),
]    