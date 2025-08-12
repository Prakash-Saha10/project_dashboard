from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES=[
        ('ADMIN','Admin'),
        ('DEVELOPER','Developer'),
        ('TESTER','Tester'),
        ('ANALYST','Project Analyst'),
        ('MANAGER','Project Manager'),
    ]

    role=models.CharField(max_length=20,choices=ROLE_CHOICES)
    profile_pic=models.ImageField(upload_to='profile_pics/',blank=True,null=True)
    phone=models.CharField(max_length=20,blank=True,null=True)

    def __str__(self):
        return f'{self.username}({self.get_role_display()})'