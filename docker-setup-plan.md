# План настройки Docker для проекта Seabroker

## Выявленные проблемы

1. **Ошибка сборки фронтенда:** В файле `App.js` (строка 20) импортируется компонент `NotFoundPage` из './pages/NotFoundPage', но этот файл отсутствует в проекте.

```javascript
// Проблемная строка в App.js
import NotFoundPage from './pages/NotFoundPage';
```

Этот компонент используется для маршрута 404 (строка 95):

```javascript
{/* 404 Page */}
<Route path="*" element={<NotFoundPage />} />
```

## Необходимые действия

### 1. Создание страницы 404

Необходимо создать файл `NotFoundPage.js` в директории `frontend/src/pages/` со следующим содержимым:

```javascript
import React from 'react';

const NotFoundPage = () => {
  return (
    <div className="d-flex justify-content-center align-items-center flex-column">
      <h1>404</h1>
      <h2>Страница не найдена</h2>
      <p>Запрашиваемая страница не существует или была перемещена.</p>
    </div>
  );
};

export default NotFoundPage;
```

### 2. Альтернативный вариант

Если создание файла не требуется, можно модифицировать `App.js`, чтобы использовать встроенный компонент вместо импорта:

```javascript
// Удалить импорт NotFoundPage

// Заменить строку:
<Route path="*" element={<NotFoundPage />} />

// На:
<Route path="*" element={
  <div className="d-flex justify-content-center align-items-center flex-column">
    <h1>404</h1>
    <h2>Страница не найдена</h2>
    <p>Запрашиваемая страница не существует или была перемещена.</p>
  </div>
} />
```

## Запуск проекта в Docker

После решения проблемы с отсутствующим файлом, следует выполнить сборку и запуск проекта:

```bash
docker-compose up --build
```

## Доступ к приложению

После успешной сборки и запуска, приложение будет доступно по следующим адресам:

- Frontend: http://localhost
- Backend API: http://localhost/api
- Django Admin: http://localhost/admin
- MinIO консоль: http://localhost/minio (логин: seajobs, пароль: seajobs_minio_key)