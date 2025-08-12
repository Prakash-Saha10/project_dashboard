from django.db import models
from accounts.models import CustomUser
from projects.models import Task,TaskUpdate

# Create your models here.
class Notification(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='notifications')
    message=models.TextField()
    related_task=models.ForeignKey(Task,on_delete=models.CASCADE,null=True,blank=True)
    related_update=models.ForeignKey(TaskUpdate,on_delete=models.CASCADE,null=True,blank=True)
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Notification for {self.user.username}: {self.message[:50]}...'
    
    class Meta:
        ordering=['-created_at']

        
    
    