from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
   path('assigner/', views.assigner_dashboard, name='assigner_dashboard'),
    path('assignee/', views.assignee_dashboard, name='assignee_dashboard'),
    path('logout/', views.logout_user, name='logout'), 
    path('add_task/', views.add_task, name='add_task'),
    path("delete-task/", views.delete_task, name="delete_task"),
    path('clear-all-tasks/', views.clear_all_tasks, name='clear_all_tasks'),
    path("toggle-task/", views.toggle_task_completion, name="toggle_task_completion"),
   path("complete-task/<int:task_id>/", views.toggle_task_complete, name="toggle_task_complete"),
]
