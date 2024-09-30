from django.contrib import admin
from .models import Task_Model,UserProfile

# Register your models here.
admin.site.register(Task_Model)
admin.site.register(UserProfile)