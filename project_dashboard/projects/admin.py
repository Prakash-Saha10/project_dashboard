from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project, Task, TaskUpdate

class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ('title','assigned_to','status','priority','due_date')
    readonly_fields = ()

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name','manager','status','start_date','end_date','created_at')
    list_filter = ('status','start_date','end_date','manager')
    search_fields = ('name','description','manager__username')
    inlines = [TaskInline]
    filter_horizontal = ('team_members',)
    date_hierarchy = 'start_date'

class TaskUpdateInline(admin.TabularInline):
    model = TaskUpdate
    extra = 0
    readonly_fields = ('updated_by','status_before','status_after','notes','created_at')
    can_delete = False

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title','project','assigned_to','status','priority','due_date','updated_at')
    list_filter = ('status','priority','due_date','project')
    search_fields = ('title','description','assigned_to__username','project__name')
    inlines = [TaskUpdateInline]

class TaskUpdateAdmin(admin.ModelAdmin):
    list_display = ('task','updated_by','status_before','status_after','created_at')
    search_fields = ('task__title','updated_by__username','notes')
    list_filter = ('created_at',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskUpdate, TaskUpdateAdmin)
