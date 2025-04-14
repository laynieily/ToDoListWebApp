from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
   path('assigner/', views.assigner_dashboard, name='assigner_dashboard'),
    path('assignee/', views.assignee_dashboard, name='assignee_dashboard'),
    path('logout/', views.logout_user, name='logout'), 

]
