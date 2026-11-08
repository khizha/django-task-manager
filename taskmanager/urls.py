from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TaskListCreateView,
    TaskDetailView,
    task_statistics,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    CategoryViewSet,
)

# настройка маршрутов для категорий
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:task_id>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/statistics/', task_statistics, name='task-statistics'),
    path(
        'subtasks/',
        SubTaskListCreateView.as_view(),
        name='subtask-list-create'
    ),
    path(
        'subtasks/<int:subtask_id>/',
        SubTaskDetailUpdateDeleteView.as_view(),
        name='subtask-detail-update-delete'
    ),
    path('', include(router.urls)),
]
