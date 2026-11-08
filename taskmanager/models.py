from django.db import models
from django.utils import timezone

# возвращает только неудалённые категории
class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    # для мягкого удаления
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    # менеджер для мягкого удаления
    objects = SoftDeleteManager()

    class Meta:                                         # Дополнительные настройки модели Category. В нашем случае -
                                                        # Имя таблицы в базе данных: 'task_manager_category'.
                                                        # Человекочитаемое имя модели: 'Category'.
                                                        # Уникальность по полю 'name'.
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_category_name',
            ),
        ]

    def __str__(self):
        return self.name

    # при удалении фактически категории помечаем удаленными, но физически не удаляем
    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])


class Task(models.Model):
    title = models.CharField(max_length=200)             # Название задачи. Должно быть уникальным для даты. То есть,
                                                         # одинаковые названия могут быть только в разные даты.
    description = models.TextField()                     # description: Описание задачи.
    categories = models.ManyToManyField(Category)        # Категории задачи. Многие ко многим.
    status = models.CharField(                           # Статус задачи.
        max_length=20,
        choices=[
            ('new', 'New'),
            ('in_progress', 'In progress'),
            ('pending', 'Pending'),
            ('blocked', 'Blocked'),
            ('done', 'Done'),
        ],
        default='new',
    )
    deadline = models.DateTimeField()                    # Дата и время дедлайна.
    created_at = models.DateTimeField(auto_now_add=True) # Дата и время создания. Заполненяется автоматически при
                                                         # создании объекта.

    created_date = models.DateField(auto_now_add=True)  # Дата создания объекта - для проверки уникальности.

    class Meta:                                         # Дополнительные настройки модели Task. В нашем случае -
                                                        # Имя таблицы в базе данных: 'task_manager_task'.
                                                        # Сортировка по убыванию даты создания.
                                                        # Человекочитаемое имя модели: 'Task'.
                                                        # Уникальность по полю 'title'.
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique_task_title',      # имя этого ограничения
            ),
        ]

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(max_length=200)                   # Название подзадачи.
    description = models.TextField()                           # Описание подзадачи.
    task = models.ForeignKey(Task, on_delete=models.CASCADE)   # Основная задача. Один ко многим.
    status = models.CharField(                                 # Статус задачи.
        max_length=20,
        choices=[
            ('new', 'New'),
            ('in_progress', 'In progress'),
            ('pending', 'Pending'),
            ('blocked', 'Blocked'),
            ('done', 'Done'),
        ],
        default='new',
    )
    deadline = models.DateTimeField()                         # Дата и время дедлайна.
    created_at = models.DateTimeField(auto_now_add=True)      # Дата и время создания. Заполненяется автоматически при
                                                              # создании объекта.

    class Meta:                                         # Дополнительные настройки модели SubTask. В нашем случае -
                                                        # Имя таблицы в базе данных: 'task_manager_subtask'.
                                                        # Сортировка по убыванию даты создания.
                                                        # Человекочитаемое имя модели: 'SubTask'.
                                                        # Уникальность по полю 'title'.
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique_subtask_title',
            ),
        ]

    def __str__(self):
        return self.title

