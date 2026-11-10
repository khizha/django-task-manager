"""
                            Пользователь        Администратор
Просмотр задач                  +                    +

Создание задач                  +                    +

Изменение задач                 +                    +

Удаление задач                  -                    +

Просмотр подзадач               +                    +

Создание подзадач               +                    +

Изменение подзадач              +                    +

Удаление подзадач               -                    +

Просмотр категорий              +                    +

Создание категорий              +                    +

Изменение категорий             +                    +

Удаление категорий              -                    +

Просмотр статистики             +                    +
"""

from rest_framework.permissions import BasePermission


class CustomPermission(BasePermission):
    """
    Авторизованный пользователь (не администратор) может просматривать,
    создавать и изменять объекты, просматривать статистику.

    Удалять объекты может только администратор.
    """

    def has_permission(self, request, view):

        # пользователь должен быть авторизован
        if not request.user or not request.user.is_authenticated:
            return False

        # удаление разрешено только администратору
        if request.method == 'DELETE':
            return request.user.is_staff or request.user.is_superuser

        # остальные методы разрешены авторизованным пользователям
        return True