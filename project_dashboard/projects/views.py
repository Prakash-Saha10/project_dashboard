from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Task, TaskUpdate
from .forms import ProjectForm, TaskForm, TaskUpdateForm
from notifications.models import Notification
from django.db.models import Count, Q
from django.http import JsonResponse
import json
from accounts.models import CustomUser

@login_required
def project_list(request):
    projects = Project.objects.filter(
        Q(manager=request.user) | Q(team_members=request.user)
    ).distinct().annotate(
        task_count=Count('tasks'),
        completed_task_count=Count('tasks', filter=Q(tasks__status='COMPLETED'))
    )
    
    return render(request, 'projects/project_list.html', {'projects': projects})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Project
from django.db.models import Q

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    # Authorization check
    if request.user != project.manager and request.user not in project.team_members.all():
        messages.error(request, 'You are not authorized to view this project.')
        return redirect('project_list')
    
    # All project tasks
    tasks = project.tasks.all()
    
    # Task counts
    completed_tasks = tasks.filter(status='COMPLETED').count()
    in_progress_tasks = tasks.filter(status='IN_PROGRESS').count()
    blocked_tasks = tasks.filter(status='BLOCKED').count()
    not_started_tasks = tasks.filter(status='NOT_STARTED').count()
    total_tasks = tasks.count()
    
    # Progress calculation
    progress = round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0
    
    context = {
        'project': project,
        'tasks': tasks,
        'team_members': project.team_members.all(),
        'progress': progress,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'blocked_tasks': blocked_tasks,
        'not_started_tasks': not_started_tasks,
        'total_tasks': total_tasks
    }
    
    return render(request, 'projects/project_detail.html', context)

   

@login_required
def project_create(request):
    if request.user.role not in ['ADMIN', 'MANAGER']:
        messages.error(request, 'You are not authorized to create projects.')
        return redirect('project_list')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            
            # Create notification for team members
            for member in project.team_members.all():
                Notification.objects.create(
                    user=member,
                    message=f"You have been added to project: {project.name}",
                    related_task=None
                )
            
            messages.success(request, 'Project created successfully.')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(initial={'manager': request.user})
    
    return render(request, 'projects/project_form.html', {'form': form})

@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.user != project.manager and request.user.role != 'ADMIN':
        messages.error(request, 'You are not authorized to update this project.')
        return redirect('project_list')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/project_form.html', {'form': form})

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    if request.user != project.manager and request.user.role != 'ADMIN':
        messages.error(request, 'You are not authorized to delete this project.')
        return redirect('project_list')
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully.')
        return redirect('project_list')
    
    return render(request, 'projects/project_confirm_delete.html', {'project': project})

@login_required
def task_list(request):
    tasks = Task.objects.filter(
        Q(project__manager=request.user) | 
        Q(assigned_to=request.user) | 
        Q(project__team_members=request.user)
    ).distinct()
    
    return render(request, 'projects/task_list.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    # Check authorization
    if (request.user != task.project.manager and 
        request.user != task.assigned_to and 
        request.user not in task.project.team_members.all()):
        messages.error(request, 'You are not authorized to view this task.')
        return redirect('task_list')
    
    updates = task.updates.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, task=task, user=request.user)
        if form.is_valid():
            update = form.save(commit=False)
            update.task = task
            update.updated_by = request.user
            update.status_before = task.status
            update.save()
            
            # Update task status
            task.status = update.status_after
            task.save()
            
            # Create notification for project manager
            if request.user != task.project.manager:
                Notification.objects.create(
                    user=task.project.manager,
                    message=f"{request.user.username} updated task '{task.title}' to {task.get_status_display()}",
                    related_task=task,
                    related_update=update
                )
            
            messages.success(request, 'Task updated successfully.')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskUpdateForm(task=task, user=request.user)
    
    context = {
        'task': task,
        'updates': updates,
        'form': form,
    }
    
    return render(request, 'projects/task_detail.html', context)

@login_required
def task_create(request, project_pk=None):
    if project_pk:
        project = get_object_or_404(Project, pk=project_pk)
        if request.user != project.manager and request.user.role != 'ADMIN':
            messages.error(request, 'You are not authorized to create tasks for this project.')
            return redirect('project_list')
    else:
        project = None
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            
            # Create notification for assigned user
            if task.assigned_to:
                Notification.objects.create(
                    user=task.assigned_to,
                    message=f"You have been assigned a new task: {task.title}",
                    related_task=task
                )
            
            messages.success(request, 'Task created successfully.')
            return redirect('task_detail', pk=task.pk)
    else:
        initial = {'project': project} if project else {}
        form = TaskForm(initial=initial)
    
    return render(request, 'projects/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.user != task.project.manager and request.user.role != 'ADMIN':
        messages.error(request, 'You are not authorized to update this task.')
        return redirect('task_list')
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            
            # Create notification if assigned user changed
            if 'assigned_to' in form.changed_data and task.assigned_to:
                Notification.objects.create(
                    user=task.assigned_to,
                    message=f"You have been assigned to task: {task.title}",
                    related_task=task
                )
            
            messages.success(request, 'Task updated successfully.')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'projects/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.user != task.project.manager and request.user.role != 'ADMIN':
        messages.error(request, 'You are not authorized to delete this task.')
        return redirect('task_list')
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('project_detail', pk=task.project.pk)
    
    return render(request, 'projects/task_confirm_delete.html', {'task': task})

@login_required
def get_project_progress(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    # Check authorization
    if request.user != project.manager and request.user not in project.team_members.all():
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    tasks = project.tasks.all()
    status_counts = tasks.values('status').annotate(count=Count('status'))
    
    data = {
        'total_tasks': tasks.count(),
        'completed_tasks': tasks.filter(status='COMPLETED').count(),
        'status_distribution': list(status_counts),
    }
    
    return JsonResponse(data)

@login_required
def get_user_progress(request, user_id):
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    user = get_object_or_404(CustomUser, pk=user_id)
    tasks = user.tasks.all()
    status_counts = tasks.values('status').annotate(count=Count('status'))
    
    data = {
        'total_tasks': tasks.count(),
        'completed_tasks': tasks.filter(status='COMPLETED').count(),
        'status_distribution': list(status_counts),
    }
    
    return JsonResponse(data)

# projects/views.py
@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not (request.user.is_admin or request.user == project.manager):
        messages.error(request, "You don't have permission!")
        return redirect('project_list')
    # ... rest of the view ...