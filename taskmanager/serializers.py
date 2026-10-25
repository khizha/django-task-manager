from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Преобразовывает объекты Task в данные, которые можно передавать через API, и проверяет входящие данные.
    """
    class Meta:
        model = Task
        fields = '__all__'


