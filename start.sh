#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}██████╗ ██╗  ██╗ ██████╗ ███████╗██████╗ ██╗
██╔══██╗██║ ██╔╝██╔════╝██╔════╝██╔══██╗██║
██║  ██║█████╔╝ ██║     █████╗  ██║  ██║██║
██║  ██║██╔═██╗ ██║     ██╔══╝  ██║  ██║╚═╝
██████╔╝██║ ██║╚██████╗███████╗██████╔╝██╗
╚═════╝ ╚═╝ ╚═╝ ╚═════╝╚══════╝╚═════╝ ╚═╝${NC}"
echo -e "${YELLOW}Консоль.Про Clone - Docker Setup${NC}"
echo ""

# Проверка установки Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Ошибка: Docker не установлен${NC}"
    echo "Установите Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Проверка установки Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Ошибка: Docker Compose не установлен${NC}"
    echo "Установите Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✓${NC} Docker и Docker Compose установлены"
echo ""

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo -e "${YELLOW}ℹ Файл .env не найден. Создаю из .env.example...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✓${NC} Файл .env создан"
        echo -e "${YELLOW}⚠ Не забудьте отредактировать SECRET_KEY и пароли в .env${NC}"
    else
        echo -e "${RED}Ошибка: .env.example не найден${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓${NC} Файл .env найден"
fi
echo ""

# Остановка старых контейнеров
echo -e "${YELLOW}Останавливаю старые контейнеры...${NC}"
docker-compose down 2>/dev/null
echo ""

# Сборка образов
echo -e "${YELLOW}Сборка Docker образов...${NC}"
if docker-compose build; then
    echo -e "${GREEN}✓${NC} Образы собраны успешно"
else
    echo -e "${RED}Ошибка при сборке образов${NC}"
    exit 1
fi
echo ""

# Запуск контейнеров
echo -e "${YELLOW}Запуск контейнеров...${NC}"
if docker-compose up -d; then
    echo -e "${GREEN}✓${NC} Контейнеры запущены"
else
    echo -e "${RED}Ошибка при запуске контейнеров${NC}"
    exit 1
fi
echo ""

# Ожидание запуска сервисов
echo -e "${YELLOW}Ожидание запуска сервисов...${NC}"
sleep 10

# Проверка статуса сервисов
echo -e "${YELLOW}Проверка статуса сервисов...${NC}"
docker-compose ps
echo ""

# Информация о доступе
echo -e "${GREEN}████████████████████████████████████████████████${NC}"
echo -e "${GREEN}✓ Приложение успешно запущено!${NC}"
echo ""
echo -e "Доступ к приложению:"
echo -e "  ${GREEN}•${NC} API:              http://localhost:8000/api/"
echo -e "  ${GREEN}•${NC} Admin:            http://localhost:8000/admin/"
echo -e "  ${GREEN}•${NC} API Docs:         http://localhost:8000/api/schema/swagger-ui/"
echo ""
echo -e "Полезные команды:"
echo -e "  ${YELLOW}•${NC} Просмотр логов:        docker-compose logs -f"
echo -e "  ${YELLOW}•${NC} Остановка:            docker-compose stop"
echo -e "  ${YELLOW}•${NC} Перезапуск:           docker-compose restart"
echo -e "  ${YELLOW}•${NC} Создать superuser:    docker-compose exec backend python manage.py createsuperuser"
echo ""
echo -e "${YELLOW}⚠ Для production обязательно измените SECRET_KEY и пароли в .env!${NC}"
echo -e "${GREEN}████████████████████████████████████████████████${NC}"
