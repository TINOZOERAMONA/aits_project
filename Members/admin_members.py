# Register your models here.

from django.contrib import admin
from .models import Profile, Department, Issue

admin.site.register(Profile)
admin.site.register(Department)
admin.site.register(Issue)
