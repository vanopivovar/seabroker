from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status

# Общие ответы
unauthorized_response = OpenApiResponse(
    description="Не авторизован",
    response={
        "type": "object",
        "properties": {
            "detail": {"type": "string", "example": "Учетные данные не были предоставлены."}
        }
    }
)

forbidden_response = OpenApiResponse(
    description="Доступ запрещен",
    response={
        "type": "object",
        "properties": {
            "detail": {"type": "string", "example": "У вас нет прав для выполнения этого действия."}
        }
    }
)

not_found_response = OpenApiResponse(
    description="Ресурс не найден",
    response={
        "type": "object",
        "properties": {
            "detail": {"type": "string", "example": "Не найдено."}
        }
    }
)

validation_error_response = OpenApiResponse(
    description="Ошибка валидации",
    response={
        "type": "object",
        "properties": {
            "field_name": {
                "type": "array",
                "items": {"type": "string"},
                "example": ["Это поле обязательно."]
            }
        }
    }
)

# Декораторы для эндпоинтов
def auth_required():
    return extend_schema(
        responses={
            status.HTTP_401_UNAUTHORIZED: unauthorized_response,
            status.HTTP_403_FORBIDDEN: forbidden_response,
        },
        auth=["Bearer"]
    )

def paginated_response():
    return extend_schema(
        parameters=[
            {
                "name": "page",
                "in": "query",
                "required": False,
                "schema": {"type": "integer", "default": 1},
                "description": "Номер страницы"
            },
            {
                "name": "page_size",
                "in": "query",
                "required": False,
                "schema": {"type": "integer", "default": 10},
                "description": "Количество элементов на странице"
            }
        ]
    ) 