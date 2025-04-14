from django.shortcuts import redirect, render
from django.contrib import messages
from .models import CustomUser, Task
from django.http import JsonResponse
from .models import Task

def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        role = request.POST.get('role')

        if 'register' in request.POST:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "⚠️ Username already exists.")
            else:
                CustomUser.objects.create(username=username, role=role)
                messages.success(request, "✅ Registered! You can now log in.")
            return redirect('home')

        elif 'login' in request.POST:
            try:
                user = CustomUser.objects.get(username=username, role=role)
                request.session['user_id'] = user.id
                if role == 'assigner':
                    return redirect('assigner_dashboard')
                elif role == 'assignee':
                    return redirect('assignee_dashboard')
            except CustomUser.DoesNotExist:
                messages.error(request, "❌ User not found or role mismatch.")
                return redirect('home')

    return render(request, 'home.html')




def assigner_dashboard(request):
    if not request.session.get('user_id'):
        return redirect('home')

    if request.method == 'POST':
        text = request.POST.get('task')
        due_date = request.POST.get('due_date')
        if text:
            Task.objects.create(text=text, due_date=due_date or None)

    tasks = Task.objects.filter(deleted=False).order_by('-created_at')
    return render(request, 'home.html', {'tasks': tasks})


def assignee_dashboard(request):
    if not request.session.get('user_id'):
        return redirect('home')

    tasks = Task.objects.filter(deleted=False).order_by('-created_at')
    return render(request, 'assignee.html', {'tasks': tasks})


def logout_user(request):
    request.session.flush()
    return redirect('home')

