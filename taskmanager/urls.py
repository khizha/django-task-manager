from django.urls import path
from .views import task_create, tasks_get_all, task_get_one, task_statistics

urlpatterns = [
    path('tasks/create/', task_create, name='task-create'),
    path('tasks/', tasks_get_all, name='tasks-get_all'),
    path('tasks/<int:task_id>/', task_get_one, name='task-get-one'),
    path('tasks/statistics/', task_statistics, name='task-statistics'),
]
