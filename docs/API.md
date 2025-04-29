# API Документация SeaJobs

## Общая информация

- **Базовый URL**: `http://localhost/api/v1/`
- **Формат данных**: JSON
- **Аутентификация**: JWT Token

## Аутентификация

### Получение токена

```http
POST /api/v1/auth/token/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "password123"
}
```

**Ответ:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Обновление токена

```http
POST /api/v1/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Пользователи

### Регистрация пользователя

```http
POST /api/v1/users/register/
Content-Type: application/json

{
    "email": "newuser@example.com",
    "password": "password123",
    "first_name": "Иван",
    "last_name": "Иванов",
    "role": "candidate" // или "employer"
}
```

### Получение профиля пользователя

```http
GET /api/v1/users/me/
Authorization: Bearer <access_token>
```

## Вакансии

### Получение списка вакансий

```http
GET /api/v1/vacancies/
Authorization: Bearer <access_token>
```

**Параметры запроса:**
- `page` - номер страницы
- `search` - поиск по названию
- `salary_min` - минимальная зарплата
- `salary_max` - максимальная зарплата
- `experience` - требуемый опыт

### Создание вакансии

```http
POST /api/v1/vacancies/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "Капитан судна",
    "description": "Описание вакансии...",
    "salary": 150000,
    "experience": "3-5 лет",
    "requirements": ["Требование 1", "Требование 2"]
}
```

## Резюме

### Создание резюме

```http
POST /api/v1/resumes/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

{
    "title": "Резюме капитана",
    "experience": "5 лет",
    "skills": ["Навык 1", "Навык 2"],
    "file": <файл резюме>
}
```

### Поиск резюме

```http
GET /api/v1/resumes/
Authorization: Bearer <access_token>
```

**Параметры запроса:**
- `search` - поиск по навыкам
- `experience` - требуемый опыт
- `salary_min` - минимальная зарплата

## Заявки на вакансии

### Отправка заявки

```http
POST /api/v1/applications/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "vacancy_id": 1,
    "message": "Сопроводительное письмо..."
}
```

### Получение списка заявок

```http
GET /api/v1/applications/
Authorization: Bearer <access_token>
```

## Сообщения

### Отправка сообщения

```http
POST /api/v1/messages/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "recipient_id": 1,
    "content": "Текст сообщения..."
}
```

### Получение диалога

```http
GET /api/v1/messages/conversation/{user_id}/
Authorization: Bearer <access_token>
```

## Коды ошибок

- `400` - Неверный запрос
- `401` - Не авторизован
- `403` - Доступ запрещен
- `404` - Ресурс не найден
- `500` - Внутренняя ошибка сервера 