from django.shortcuts import redirect, render
from django.contrib import messages
from .models import CustomUser, Task
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Task

def home(request):
    if not request.session.get('user_id'):
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
                    return redirect('assigner_dashboard') if role == 'assigner' else redirect('assignee_dashboard')
                except CustomUser.DoesNotExist:
                    messages.error(request, "❌ User not found or role mismatch.")
                    return redirect('home')

        return render(request, 'home.html')  

    
    user = CustomUser.objects.get(id=request.session['user_id'])
    return redirect('assigner_dashboard') if user.role == 'assigner' else redirect('assignee_dashboard')


def assigner_dashboard(request):
    if not request.session.get('user_id'):
        return redirect('home')

    if request.method == 'POST':
        text = request.POST.get('task')
        due_date = request.POST.get('due_date')

        if text:
            assigner = CustomUser.objects.get(id=request.session['user_id'])
            Task.objects.create(
                text=text,
                due_date=due_date or None,
                assigner=assigner,
            )
            messages.success(request, "✅ Task created successfully.")
        else:
            messages.error(request, "⚠️ Task text is required.")

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


@csrf_exempt
def delete_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get("id")
        try:
            task = Task.objects.get(id=task_id)
            task.deleted = True
            task.save()
            return JsonResponse({"success": True})
        except Task.DoesNotExist:
            return JsonResponse({"success": False, "error": "Task not found"}, status=404)
@csrf_exempt
def clear_all_tasks(request):
    if request.method == 'POST':
        Task.objects.all().delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid_method'}, status=400)
@csrf_exempt
def add_task(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'status': 'not_logged_in'})

        data = json.loads(request.body)
        text = data.get('text')
        due_date = data.get('due_date')

        user = CustomUser.objects.get(id=user_id)

        Task.objects.create(
            text=text,
            due_date=due_date or None,
            assigner=user  
        )

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid_method'})
@csrf_exempt
def toggle_task_completion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('id')
        completed = data.get('completed')

        try:
            task = Task.objects.get(id=task_id)
            task.completed = completed
            task.save()
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)
@csrf_exempt
def complete_task(request, task_id):
    if request.method == 'POST':
        try:
            task = Task.objects.get(id=task_id)
            task.completed = not task.completed
            task.save()
            return JsonResponse({'completed': task.completed})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
@csrf_exempt
def toggle_task_complete(request, task_id):
    if request.method == "POST":
        try:
            task = Task.objects.get(id=task_id)
            task.completed = not task.completed
            task.save()
            return JsonResponse({'completed': task.completed})
        except Task.DoesNotExist:
            return JsonResponse({'error': 'Task not found'}, status=404)
    return JsonResponse({'error': 'Invalid method'}, status=405)
        