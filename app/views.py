from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from .forms import SignUpForm

def home(request):
		if request.method == "POST":
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(request, username = username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, "Login Successful")
				return redirect('home')
			else:
				messages.success(request, "Login Error")
				return redirect('home')
		else:
			return render(request, 'home.html',{})


#def login_user(request):
#	pass

def logout_user(request):
	logout(request)
	messages.success(request,"Logged out")
	return redirect('home')

def register_user(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user = authenticate(request, username=form.cleaned_data['username'],
			                    password=form.cleaned_data['password1'])
			if user is not None:
				login(request, user)
				return redirect('home')
		else:
			print("Form errors:", form.errors)  # ✅ Debug output
	else:
		form = SignUpForm()
	return render(request, 'register.html', {'form': form})

