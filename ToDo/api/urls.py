from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('form-login/', views.form_login),
    path('form-alter/<int:pk>/', views.form_alter),
    path('form-create/', views.form_create),
    path('login/', views.login, name='login'),
    path('logout/', views.logout),
    path('todo/', views.taskLists, name='create'),
    path('todo/<int:pk>/', views.task_list_detail, name='alter'),
    path('todo/<int:pk>/execute/', views.ExecuteTask, name='execute'),
]