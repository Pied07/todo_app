from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Task_Model(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    task_name = models.CharField(max_length=150)
    task_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.task_name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    apikey = models.TextField(null=True)
    accesskey = models.TextField(null=True)

    def __str__(self):
        return self.user.username