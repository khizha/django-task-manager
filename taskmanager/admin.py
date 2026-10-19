from django.contrib import admin
from .models import Category, Task, SubTask

class SubTaskInline(admin.TabularInline):
    """
    Cоздаёт инлайн-форму, которая отображает подзадачи в табличном формате
    """
    model = SubTask # редактируем объекты модели SubTask
    extra = 1       # показать одну пустую форму для создания новой подзадачи

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'status', 'deadline', 'created_at')
    inlines = [SubTaskInline]   # отображать на странице задачи связвнные с ней подзадачи

    def short_title(self, obj):
        if len(obj.title) > 10:
            return obj.title[:10] + '...'
        return obj.title

    short_title.short_description = 'Title'

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'status', 'deadline', 'created_at')

    def set_status_done(self, request, queryset):
        queryset.update(status='done')

    set_status_done.short_description = 'Set selected subtasks status to Done'

    actions = [set_status_done]

