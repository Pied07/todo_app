from rest_framework import serializers
from .models import Task_Model

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_Model
        fields = '__all__'