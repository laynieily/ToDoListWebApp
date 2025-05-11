from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard_view, name='dashboard'),
    path('create/', views.create_task, name='create_task'),
    path('task/<int:task_id>/', views.task_detail_view, name='task_detail'),
    path('update_status/<int:task_id>/', views.update_status_view, name='update_status'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task_view, name='delete_task'),
]





