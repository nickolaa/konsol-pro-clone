# Запуск проекта в Docker

## Предварительные требования

- Docker версии 20.10+
- Docker Compose версии 2.0+

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/nickolaa/konsol-pro-clone.git
cd konsol-pro-clone
```

### 2. Создание файла окружения

```bash
cp .env.example .env
```

Отредактируйте `.env` при необходимости, особенно:
- `SECRET_KEY` - измените на уникальный ключ
- `DEBUG` - установите `False` для production
- `POSTGRES_PASSWORD` - измените пароль БД

### 3. Запуск контейнеров

#### Первый запуск (с миграциями)

```bash
docker-compose up --build -d
```

Команда выполнит:
1. Сборку Docker-образов
2. Запуск PostgreSQL и Redis
3. Применение миграций Django
4. Сбор статических файлов
5. Запуск приложения

#### Последующие запуски

```bash
docker-compose up -d
```

### 4. Создание суперпользователя

```bash
docker-compose exec backend python manage.py createsuperuser
```

## Доступ к приложению

- **API**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/schema/swagger-ui/

## Полезные команды

### Просмотр логов

```bash
# Все сервисы
docker-compose logs -f

# Конкретный сервис
docker-compose logs -f backend
docker-compose logs -f celery
```

### Выполнение команд Django

```bash
# Миграции
docker-compose exec backend python manage.py migrate

# Создание миграций
docker-compose exec backend python manage.py makemigrations

# Django shell
docker-compose exec backend python manage.py shell

# Сбор статики
docker-compose exec backend python manage.py collectstatic --noinput
```

### Работа с базой данных

```bash
# Подключение к PostgreSQL
docker-compose exec db psql -U konsol_user -d konsol_db

# Создание резервной копии
docker-compose exec db pg_dump -U konsol_user konsol_db > backup.sql

# Восстановление из резервной копии
docker-compose exec -T db psql -U konsol_user -d konsol_db < backup.sql
```

### Управление контейнерами

```bash
# Остановка
docker-compose stop

# Перезапуск
docker-compose restart

# Перезапуск конкретного сервиса
docker-compose restart backend

# Остановка и удаление контейнеров
docker-compose down

# Удаление с вольюмами (ОСТОРОЖНО: удаляет данные!)
docker-compose down -v
```

### Пересборка образов

```bash
# Пересборка всех образов
docker-compose build --no-cache

# Пересборка конкретного сервиса
docker-compose build --no-cache backend
```

## Архитектура контейнеров

### Сервисы

1. **db** - PostgreSQL 15
   - Порт: 5432
   - Вольюм: `postgres_data`

2. **redis** - Redis 7
   - Порт: 6379
   - Вольюм: `redis_data`

3. **backend** - Django приложение
   - Порт: 8000
   - Вольюмы: код приложения, статика, медиа

4. **celery** - Celery worker
   - Асинхронные задачи

5. **celery-beat** - Celery Beat scheduler
   - Периодические задачи

### Вольюмы

- `postgres_data` - данные PostgreSQL
- `redis_data` - данные Redis
- `static_volume` - статические файлы Django
- `media_volume` - загруженные пользователями файлы

### Сеть

Все сервисы работают в единой сети `konsol_network` с драйвером bridge.

## Отладка

### Проблемы с подключением к БД

Если backend не может подключиться к базе данных:

```bash
# Проверьте статус БД
docker-compose ps db

# Проверьте логи БД
docker-compose logs db

# Перезапустите backend
docker-compose restart backend
```

### Проблемы с миграциями

```bash
# Вручную примените миграции
docker-compose exec backend python manage.py migrate

# Проверьте статус миграций
docker-compose exec backend python manage.py showmigrations
```

### Очистка и полный перезапуск

```bash
# Остановка и удаление всех контейнеров и вольюмов
docker-compose down -v

# Удаление образов
docker-compose down --rmi all

# Полная пересборка и запуск
docker-compose build --no-cache
docker-compose up -d
```

## Production развертывание

Для production-среды рекомендуется:

1. Изменить `DEBUG=False` в `.env`
2. Установить сильный `SECRET_KEY`
3. Настроить `ALLOWED_HOSTS` с вашими доменами
4. Использовать HTTPS
5. Добавить Nginx как reverse proxy
6. Настроить регулярные бекапы БД
7. Использовать внешние вольюмы для данных
8. Настроить мониторинг и логирование

## Требования к ресурсам

Минимальные рекомендуемые ресурсы:

- **CPU**: 2 ядра
- **RAM**: 4 GB
- **Disk**: 10 GB свободного места

## Поддержка

При возникновении проблем создайте issue в репозитории с описанием проблемы и логами.
