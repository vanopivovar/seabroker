# Руководство по развертыванию SeaJobs

## Требования к серверу

- Ubuntu 20.04 LTS или новее
- 2+ CPU ядра
- 4+ GB RAM
- 20+ GB SSD
- Docker и Docker Compose
- Nginx (опционально, для проксирования)

## Подготовка сервера

1. Обновите систему:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Установите Docker и Docker Compose:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

3. Установите Nginx:
   ```bash
   sudo apt install nginx -y
   ```

## Настройка окружения

1. Создайте директорию для проекта:
   ```bash
   mkdir -p /opt/seajobs
   cd /opt/seajobs
   ```

2. Склонируйте репозиторий:
   ```bash
   git clone <url-репозитория> .
   ```

3. Создайте файл `.env`:
   ```bash
   cp .env.example .env
   ```

4. Отредактируйте `.env`:
   ```bash
   nano .env
   ```

   Установите следующие переменные:
   ```
   DEBUG=0
   SECRET_KEY=<сгенерированный-секретный-ключ>
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   DATABASE_URL=postgres://user:password@db:5432/seajobs
   MINIO_ACCESS_KEY=<access-key>
   MINIO_SECRET_KEY=<secret-key>
   ```

## Настройка SSL

1. Установите Certbot:
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   ```

2. Получите сертификат:
   ```bash
   sudo certbot --nginx -d your-domain.com -d www.your-domain.com
   ```

## Настройка Nginx

1. Создайте конфигурацию:
   ```bash
   sudo nano /etc/nginx/sites-available/seajobs
   ```

2. Добавьте конфигурацию:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com www.your-domain.com;
       return 301 https://$server_name$request_uri;
   }

   server {
       listen 443 ssl;
       server_name your-domain.com www.your-domain.com;

       ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /static/ {
           alias /opt/seajobs/backend/static/;
       }

       location /media/ {
           alias /opt/seajobs/backend/media/;
       }
   }
   ```

3. Активируйте конфигурацию:
   ```bash
   sudo ln -s /etc/nginx/sites-available/seajobs /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Развертывание приложения

1. Соберите frontend:
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

2. Запустите Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. Создайте суперпользователя:
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

4. Соберите статические файлы:
   ```bash
   docker-compose exec backend python manage.py collectstatic --noinput
   ```

## Мониторинг и обслуживание

### Логи

Просмотр логов:
```bash
docker-compose logs -f
```

### Резервное копирование

1. Создайте скрипт для резервного копирования:
   ```bash
   nano /opt/seajobs/backup.sh
   ```

2. Добавьте содержимое:
   ```bash
   #!/bin/bash
   BACKUP_DIR="/opt/seajobs/backups"
   DATE=$(date +%Y-%m-%d_%H-%M-%S)

   mkdir -p $BACKUP_DIR

   # Резервное копирование базы данных
   docker-compose exec -T db pg_dump -U postgres seajobs > $BACKUP_DIR/db_$DATE.sql

   # Резервное копирование медиафайлов
   tar -czf $BACKUP_DIR/media_$DATE.tar.gz backend/media/

   # Удаление старых бэкапов (старше 30 дней)
   find $BACKUP_DIR -type f -mtime +30 -delete
   ```

3. Сделайте скрипт исполняемым:
   ```bash
   chmod +x backup.sh
   ```

4. Добавьте в crontab:
   ```bash
   crontab -e
   ```
   Добавьте строку:
   ```
   0 2 * * * /opt/seajobs/backup.sh
   ```

### Обновление

1. Остановите контейнеры:
   ```bash
   docker-compose down
   ```

2. Обновите код:
   ```bash
   git pull
   ```

3. Пересоберите контейнеры:
   ```bash
   docker-compose build
   ```

4. Запустите контейнеры:
   ```bash
   docker-compose up -d
   ```

5. Примените миграции:
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

6. Соберите статические файлы:
   ```bash
   docker-compose exec backend python manage.py collectstatic --noinput
   ``` 