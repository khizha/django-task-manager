import logging

# получение логгера для HTTP-запросов
logger = logging.getLogger('django.http')


class HTTPLoggingMiddleware:
    # инициализация middleware
    def __init__(self, get_response):
        self.get_response = get_response

    # обработка HTTP-запроса и получение ответа
    def __call__(self, request):
        response = self.get_response(request)

        # запись метода, адреса и статуса ответа
        logger.info(
            '%s %s %s',
            request.method,
            request.get_full_path(),
            response.status_code
        )

        return response