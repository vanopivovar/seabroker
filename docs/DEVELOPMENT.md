# Руководство по разработке SeaJobs

## Настройка окружения разработки

### Требования

- Python 3.8+
- Node.js 16+
- Docker
- Docker Compose
- Git

### Установка зависимостей

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# или
.\venv\Scripts\activate  # для Windows
pip install -r requirements.txt
```

#### Frontend

```bash
cd frontend
npm install
```

## Запуск в режиме разработки

### Backend

```bash
cd backend
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm start
```

## Структура проекта

### Backend (Django)

```
backend/
├── apps/
│   ├── accounts/         # Аутентификация и пользователи
│   ├── applications/     # Заявки на вакансии
│   ├── core/            # Общие функции и утилиты
│   ├── messages/        # Сообщения между пользователями
│   ├── resumes/         # Резюме соискателей
│   └── vacancies/       # Вакансии
└── seajobs/            # Основной модуль проекта
```

### Frontend (React)

```
frontend/
├── src/
│   ├── components/      # Переиспользуемые компоненты
│   ├── pages/          # Страницы приложения
│   ├── services/       # API клиенты
│   ├── store/          # Управление состоянием
│   └── utils/          # Вспомогательные функции
└── public/             # Статические файлы
```

## Стиль кода

### Backend

- Используйте Black для форматирования Python кода
- Следуйте PEP 8
- Используйте docstrings для документации функций и классов

### Frontend

- Используйте Prettier для форматирования
- Следуйте ESLint правилам
- Используйте TypeScript для типизации

## Тестирование

### Backend

```bash
cd backend
python manage.py test
```

### Frontend

```bash
cd frontend
npm test
```

## Git Workflow

1. Создайте новую ветку для каждой задачи:
   ```bash
   git checkout -b feature/название-задачи
   ```

2. Коммитьте изменения:
   ```bash
   git add .
   git commit -m "Описание изменений"
   ```

3. Отправьте изменения в репозиторий:
   ```bash
   git push origin feature/название-задачи
   ```

4. Создайте Pull Request в основной ветке

## Развертывание

### Локальное развертывание

```bash
./run-local.sh
```

### Production развертывание

1. Обновите переменные окружения в `.env`
2. Соберите frontend:
   ```bash
   cd frontend
   npm run build
   ```
3. Запустите Docker Compose:
   ```bash
   docker-compose up -d
   ```

## Отладка

### Backend

- Используйте `pdb` или `ipdb` для отладки
- Проверяйте логи в `backend/logs/`

### Frontend

- Используйте React Developer Tools
- Проверяйте консоль браузера
- Используйте Redux DevTools для отладки состояния

## Безопасность

- Никогда не коммитьте секретные ключи
- Используйте `.env` для конфиденциальных данных
- Регулярно обновляйте зависимости
- Проверяйте код на уязвимости

## Мониторинг

- Проверяйте логи приложения
- Используйте Sentry для отслеживания ошибок
- Мониторьте производительность через New Relic или аналогичные инструменты 