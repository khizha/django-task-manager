"""

                            Пользователь        Администратор

Просмотр своих задач              +                    +
Просмотр чужих задач              -                    +

Создание задач                    +                    +

Изменение своих задач             +                    +
Изменение чужих задач             -                    -

Удаление своих задач              +                    +
Удаление чужих задач              -                    -

Просмотр своих подзадач           +                    +
Просмотр чужих подзадач           -                    +

Создание подзадач                 +                    +

Изменение своих подзадач          +                    +
Изменение чужих подзадач          -                    -

Удаление своих подзадач           +                    +
Удаление чужих подзадач           -                    -

Просмотр категорий                +                    +
Создание категорий                +                    +
Изменение категорий               +                    +
Удаление категорий                -                    +

Просмотр статистики               +                    +
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


class CustomPermission(BasePermission):
    """
    Проверяет авторизацию пользователя.
    Удаление категорий разрешено только администратору.
    Остальные действия разрешены авторизованным пользователям.
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


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешает просмотр объектов авторизованным пользователям.
    Изменять и удалять объект может только его владелец.
    """

    def has_permission(self, request, view):
        # пользователь должен быть авторизован
        return (
                request.user
                and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        # просмотр разрешён
        if request.method in SAFE_METHODS:
            return True

        # изменение и удаление разрешены только владельцу
        return obj.owner == request.user