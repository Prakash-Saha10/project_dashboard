from django import forms
from .models import Project,Task,TaskUpdate
from accounts.models import CustomUser

class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields=['name','description','start_date','end_date','status','manager','team_members']
        widgets={
            'start_date':forms.DateInput(attrs={'type':'date'}),
            'end_date':forms.DateInput(attrs={'type':'date'}),
            'team_members':forms.SelectMultiple(attrs={'class':'select2'}),
        }


        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.fields['manager'].queryset=CustomUser.objects.filter(role__in=['ADMIN','MANAGER'])



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'title', 'description', 'assigned_to', 'status', 'priority', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = TaskUpdate
        fields = ['status_after', 'notes']
        
    def __init__(self, *args, **kwargs):
        self.task = kwargs.pop('task', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.task:
            self.fields['status_after'].initial = self.task.status