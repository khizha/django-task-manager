from django.utils import timezone
from django.db.models import Count

from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from .models import Task, SubTask, Category
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
    CategorySerializer,
)
from .permissions import CustomPermission, IsOwnerOrReadOnly


# Create your views here.

# CRUD для категорий
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CustomPermission]

    # количества задач, связанных с каждой категорией
    @action(detail=False, methods=['get'])
    def count_tasks(self, request):
        categories = Category.objects.annotate(
            tasks_count=Count('task')
        )

        data = [
            {
                'id': category.id,
                'name': category.name,
                'tasks_count': category.tasks_count,
            }
            for category in categories
        ]

        return Response(data)


# получение списка задач и создание новой задачи
class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = [IsOwnerOrReadOnly]

    # фильтрация по статусу и дедлайну
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']

    # поиск по названию и описанию задачи
    search_fields = ['title', 'description']

    # сортировка по дате создания
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer

    # автоматическое назначение владельца задаси при создании
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Task.objects.all()

        return Task.objects.filter(owner=user)



# получение, обновление и удаление одной задачи
class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_url_kwarg = 'task_id' # id задачи будет передаваться как параметр task_id в url. если задача gj id не будет
                                 # найдена, то Generic View сам вернёт 404

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Task.objects.all()

        return Task.objects.filter(owner=user)


# получение задач текущего пользователя
class UserTaskListView(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Task.objects.all()

        return Task.objects.filter(owner=user)


# Получение статистики по задачам
@api_view(['GET'])
@permission_classes([CustomPermission])
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



# Настройка пагинации для подзадач
class SubTaskPagination(PageNumberPagination):
    page_size = 3


# Получение списка подзадач и создание новой подзадачи
class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    # пагинация: по 3 подзадачи на странице
    pagination_class = SubTaskPagination

    # фильтрация, поиск и сортировка
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # фильтрация по статусу и дедлайну
    filterset_fields = ['status', 'deadline']

    # поиск по названию и описанию
    search_fields = ['title', 'description']

    # сортировка по дате создания
    ordering_fields = ['created_at']

    # сериализатор - в зависимости от метода запроса
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer

    # автоматическая привязка подзадачи к текущему пользователю при создании подзадачи
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return SubTask.objects.all()

        return SubTask.objects.filter(owner=user)


# Получение, обновление и удаление одной подзадачи
class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    lookup_url_kwarg = 'subtask_id'

    # сериализатор - в зависимости от метода запроса
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SubTaskCreateSerializer
        return SubTaskSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return SubTask.objects.all()

        return SubTask.objects.filter(owner=user)
