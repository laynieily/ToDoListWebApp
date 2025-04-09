from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('',views.home, name = 'home'),
	path('login/',views.home, name = 'login'),
	path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
	path('register/', views.register_user, name = 'register'),

]