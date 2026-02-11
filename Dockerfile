FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Создание директории приложения
WORKDIR /app

# Копирование requirements
COPY requirements.txt /app/

# Установка зависимостей
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn

# Копирование кода проекта
COPY . /app/

# Создание пользователя для запуска приложения
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

# Создание директорий для статики и медиа
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app/staticfiles /app/media

USER appuser

# Открытие порта
EXPOSE 8000

# Скрипт запуска будет определен в docker-compose.yml
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
