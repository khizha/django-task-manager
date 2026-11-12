from django.utils import timezone

from rest_framework import serializers
from .models import Task, SubTask, Category


class TaskSerializer(serializers.ModelSerializer):
    """
    Преобразовывает объекты Task в данные, которые можно передавать через API, и проверяет входящие данные.
    """
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner']


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner']

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                'Дата deadline не может быть в прошлом.'
            )

        return value


class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['owner']

    def validate_task(self, value):
        user = self.context['request'].user

        if value.owner != user:
            raise serializers.ValidationError(
                'Нельзя создавать подзадачи для чужих задач.'
            )

        return value


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data.get('name')

        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError(
                {'name': 'Категория с таким названием уже существует.'}
            )

        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)

        if Category.objects.filter(name=name).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError(
                {'name': 'Категория с таким названием уже существует.'}
            )

        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SubTaskSerializer(serializers.ModelSerializer):
    """
        сериализатор, который определяет, какие поля каждой подзадачи показывать
    """
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['owner']


class TaskDetailSerializer(serializers.ModelSerializer):
    """
        cериализатор показывает все подзадачи, связанные с данной задачей
    """
    subtask_set = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

