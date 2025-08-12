from django.urls import path
from . import views

urlpatterns = [
    # Projects
    path('', views.project_list, name='project_list'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/update/', views.project_update, name='project_update'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),
    
    # Tasks
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('projects/<int:project_pk>/tasks/create/', views.task_create, name='project_task_create'),
    
    # API endpoints
    path('api/project/<int:project_id>/progress/', views.get_project_progress, name='project_progress'),
    path('api/user/<int:user_id>/progress/', views.get_user_progress, name='user_progress'),
]