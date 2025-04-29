from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework import status

@csrf_exempt
def csrf_failure(request, reason=""):
    """
    Обработчик ошибок CSRF.
    Возвращает JSON-ответ с информацией об ошибке.
    """
    return JsonResponse(
        {
            'detail': 'CSRF-токен отсутствует или недействителен',
            'code': 'csrf_failure',
            'status': status.HTTP_403_FORBIDDEN
        },
        status=status.HTTP_403_FORBIDDEN
    ) 