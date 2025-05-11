from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseForbidden
from .forms import SignUpForm, TaskForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Task, TaskStatus, CustomUser

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard_view(request):
    if request.user.role == 'assignee':
        tasks = Task.objects.filter(assigned_to=request.user)
        for task in tasks:
            TaskStatus.objects.get_or_create(task=task, user=request.user)
    else:
        tasks = Task.objects.all()
    return render(request, 'dashboard.html', {'tasks': tasks})


@login_required
def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})


@login_required
@require_POST
def update_status_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user not in task.assigned_to.all():
        return HttpResponseForbidden()

    new_status = request.POST.get('status')
    if new_status in ['Not started', 'In progress', 'Completed']:
        ts, _ = TaskStatus.objects.get_or_create(task=task, user=request.user)
        ts.status = new_status
        ts.save()

    return redirect('dashboard')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.user.role != 'assigner' or task.assigner != request.user:
        messages.warning(request, "You can't edit a task you didn't create.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            old_assignees = set(task.assigned_to.all())
            new_task = form.save(commit=False)
            new_assignees = set(form.cleaned_data['assigned_to'])

            # Save the task to apply form updates
            new_task.save()
            form.save_m2m()

            # Detect new assignees
            added_assignees = new_assignees - old_assignees

            # Assign default status to new assignees
            for user in added_assignees:
                TaskStatus.objects.get_or_create(task=task, user=user, defaults={'status': 'Not started'})

            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {'form': form, 'task': task})

@login_required
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    # Only assigners can delete tasks
    if request.user.role != 'assigner' or task.assigner != request.user:
        messages.warning(request, "You can't delete a task you didn't create.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        task.delete()
        return redirect('dashboard')

    return render(request, 'delete_task.html', {'task': task})


@login_required
def create_task(request):
    if request.user.role != 'assigner':
        return redirect('dashboard')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigner = request.user
            task.save()
            form.save_m2m()

            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'create_task.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
