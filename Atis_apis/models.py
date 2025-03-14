# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model extending Django's AbstractUser
class User(AbstractUser):
    # Additional fields for User
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, related_name='users')
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, related_name='users')

    def __str__(self):
        return self.username

# Role model
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Department model
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Issue model
class Issue(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Closed', 'Closed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_issues')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_issues')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='issues')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
