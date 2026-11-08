from rest_framework.pagination import CursorPagination


# пагинация с использованием курсора
class CustomCursorPagination(CursorPagination):
    page_size = 6
    ordering = 'id'