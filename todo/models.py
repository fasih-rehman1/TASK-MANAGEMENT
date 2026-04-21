from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserRole(models.TextChoices):
    SUPERADMIN = 'superadmin', 'Super Admin'
    ADMIN = 'admin','Admin'
    MANAGER = 'manager','Manager'
    USER = 'user','User'
     
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=UserRole.choices, default = UserRole.USER)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos', null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    
    
    
# class Employee(models.Model):
#     username = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#     department = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.username
    