from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    TaskListCreateView,
    TaskDetailView,
    task_statistics,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    CategoryViewSet,
    UserTaskListView,
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

    # Получение пары JWT-токенов (Access и Refresh)
    # принимает имя пользователя и пароль, возвращает Access и Refresh
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    # Обновление Access-токена с помощью Refresh-токена
    # принимает Refresh-токен и возвращает новый Access-токен
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    # Получение задач текущего пользователя
    path(
        'user-tasks/',
        UserTaskListView.as_view(),
        name='user-tasks'
    ),
]
