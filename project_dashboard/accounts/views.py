from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileUpdateForm
from .models import CustomUser
from projects.models import Project,Task
from notifications.models import Notification
from django.db.models import Count,Q
from django.utils import timezone


from django.contrib.auth.decorators import login_required

# Create your views here.
# accounts/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration Successful')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()  # show empty form on GET

    return render(request, 'accounts/register.html', {'form': form})

        

def user_login(request):
    if request.method == 'POST':
        username =request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request,'invalid username or password')
    return render(request,'accounts/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    is_admin = user.role == 'ADMIN'
    is_manager = user.role == 'MANAGER'

    if is_admin:
        projects = Project.objects.all().annotate(
            completed_tasks_count=Count('tasks', filter=Q(tasks__status='COMPLETED')),
            total_tasks_count=Count('tasks')
        )
    else:
        projects = user.projects.all().annotate(
            completed_tasks_count=Count('tasks', filter=Q(tasks__status='COMPLETED')),
            total_tasks_count=Count('tasks')
        )

    tasks = user.tasks.all()
    today = timezone.now().date()
    tasks_completed = tasks.filter(status='COMPLETED').count()
    tasks_in_progress = tasks.filter(status='IN_PROGRESS').count()
    tasks_overdue = tasks.filter(
        Q(status='IN_PROGRESS') | Q(status='NOT_STARTED'),
        due_date__lt=today
    ).count()
    tasks_not_started = tasks.filter(status='NOT_STARTED').count()

    recent_activities = [
        {"icon": "tasks", "color": "primary", "message": "Project Alpha updated", "timestamp": timezone.now()},
        {"icon": "check-circle", "color": "success", "message": "Task XYZ completed", "timestamp": timezone.now()},
    ]

    context = {
        'projects': projects,
        'tasks': tasks,
        'tasks_completed': tasks_completed,
        'tasks_in_progress': tasks_in_progress,
        'tasks_overdue': tasks_overdue,
        'tasks_not_started': tasks_not_started,
        'notifications': user.notifications.filter(is_read=False).order_by('-created_at')[:5],
        'is_admin': is_admin,
        'is_manager': is_manager,
        'recent_activities': recent_activities
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile has been updated!')
            return redirect('profile')  # Make sure 'Profile' matches your URL name
    else:
        form = ProfileUpdateForm(instance=request.user)

    # ✅ Always return a response regardless of POST validity
    return render(request, 'accounts/profile.html', {'form': form})





@login_required
def user_list(request):
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        messages.error(request,'You are not authorized to view the page')
        return redirect('dashboard')
    
    users=CustomUser.objects.all()
    return render(request,'accounts/user_list.html',{'users':users})
    
@login_required
def user_list(request,pk):
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        messages.error(request,'You are not authorized to view the page')
        return redirect('dashboard')
    user=CustomUser.objects.get(pk=pk)
    projects=user.projects.all()
    tasks=user.tasks.all()

    return render(request, 'accounts/user_detail.html', {
        'user': user,
        'projects': projects,
        'tasks': tasks,
    })

@login_required
def user_create(request):
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('dashboard')
    
    if request.method == 'POST':
       form =CustomUserCreationForm(request.POST,request.FILES)
       if form.is_valid():
           form.save()
           messages.success(request,'User Created Successfully')
           return redirect('user_list')
       else:
           form =CustomUserCreationForm()
        
    return render(request,'accounts/user_form.html',{'form':form})
    


@login_required
def user_update(request, pk):
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('dashboard')
    
    user = CustomUser.objects.get(pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'accounts/user_form.html', {'form': form})

@login_required
def user_delete(request, pk):
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        messages.error(request, 'You are not authorized to view this page.')
        return redirect('dashboard')
    
    user=CustomUser.objects.get(pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request,'User Deleted Successfully')
        return redirect('user_list')
    
    return render(request,'accounts/user_confirm_delete.html',{'user':user})


# accounts/views.py
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "Admin access required!")
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper