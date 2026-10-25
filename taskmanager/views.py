from django.shortcuts import render

from django.utils import timezone
from django.db.models import Count

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer, SubTaskCreateSerializer

# Create your views here.

# Создание новой задачи
@api_view(['POST'])
def task_create(request):
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


task_create.cls.serializer_class = TaskSerializer #показать в маршруте поля модели Task


# Получение списка всех задач
@api_view(['GET'])
def tasks_get_all(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Получение задачи по ее ID
@api_view(['GET'])
def task_get_one(request, task_id ):
    try:
        task = Task.objects.get(pk=task_id )
    except Task.DoesNotExist:
        return Response(
            {'error': 'Задача не найдена'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = TaskSerializer(task)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Получение статистики по задачам
@api_view(['GET'])
def task_statistics(request):
    # Общее количество задач
    total_tasks = Task.objects.count()

    # Количество задач по каждому статусу
    tasks_by_status = Task.objects.values('status').annotate(
        count=Count('id')
    )

    # Количество просроченных задач
    outdated_tasks = Task.objects.filter(
        deadline__lt=timezone.now()
    ).exclude(
        status='done'
    ).count()

    return Response({
        'total_tasks': total_tasks,
        'tasks_by_status': {
            item['status']: item['count']
            for item in tasks_by_status
        },
        'outdated_tasks': outdated_tasks
    }, status=status.HTTP_200_OK)


class SubTaskListCreateView(APIView):

    # Получение списка всех подзадач
    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskSerializer(subtasks, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # Создание новой подзадачи
    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SubTaskDetailUpdateDeleteView(APIView):

    # Получение подзадачи по ID
    def get(self, request, subtask_id):
        try:
            subtask = SubTask.objects.get(pk=subtask_id)
        except SubTask.DoesNotExist:
            return Response(
                {'error': 'Подзадача не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SubTaskSerializer(subtask)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # Обновление подзадачи
    def put(self, request, subtask_id):
        try:
            subtask = SubTask.objects.get(pk=subtask_id)
        except SubTask.DoesNotExist:
            return Response(
                {'error': 'Подзадача не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SubTaskCreateSerializer(
            subtask,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # Удаление подзадачи
    def delete(self, request, subtask_id):
        try:
            subtask = SubTask.objects.get(pk=subtask_id)
        except SubTask.DoesNotExist:
            return Response(
                {'error': 'Подзадача не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

