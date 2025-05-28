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
    path('profile/edit', views.profile_edit, name='profile'),
    path('logout', views.logout, name='logout'),
    path('question/<int:question_id>/like', views.question_like, name='question_like'),
    path('answer/<int:answer_id>/like', views.answer_like, name='answer_like'),
    path('answer/<int:answer_id>/correct', views.correct_answer, name='correct_answer')
]   