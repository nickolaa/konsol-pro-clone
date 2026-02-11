# konsol-pro-clone

Платформа для работы с самозанятыми - аналог Консоль.Про. Автоматизация заданий, документооборота и выплат.

## Текущий статус

### Реализовано

#### ✅ Задача 4: Авторизация и регистрация пользователей (Frontend)
**Создана полная система авторизации на frontend:**
1. **Redux Store для авторизации** (`frontend/src/features/auth/authSlice.ts`)
2. **Страница входа** (`frontend/src/pages/auth/Login.tsx`)
3. **Страница регистрации** (`frontend/src/pages/auth/Register.tsx`)
4. **Маршрутизация** (`frontend/src/routes.tsx`)

#### ✅ Задача 5: Дашборд компании (Frontend)
**Реализован функциональный дашборд для компаний:**
1. **CompanyDashboard** (`frontend/src/pages/company/CompanyDashboard.tsx`)
2. **TaskManagement** (`frontend/src/pages/company/TaskManagement.tsx`)
3. **CreateTask** (`frontend/src/pages/company/CreateTask.tsx`)
4. **EditTask** (`frontend/src/pages/company/EditTask.tsx`)

#### ✅ Задача 6: Лента заданий для исполнителей (Frontend)
**Реализована полная система ленты заданий:**
1. **Redux Store для заданий** (`frontend/src/features/tasks/tasksSlice.ts`)
2. **Страница TaskFeed** (`frontend/src/pages/tasks/TaskFeed.tsx`)
3. **Страница MyTasks** (`frontend/src/pages/tasks/MyTasks.tsx`)
4. **Страница TaskHistory** (`frontend/src/pages/tasks/TaskHistory.tsx`)

#### ✅ Задача 7: Интерфейс пополнения баланса и выплат (Backend + Frontend)
**Реализована базовая система платежей и транзакций:**
1. **Модель Transaction** (`backend/models.py`)
2. **TransactionSerializer** (`backend/serializers.py`)
3. **Redux Store для платежей** (`frontend/src/features/payments/paymentsSlice.ts`)
4. **Страница Payments** (`frontend/src/pages/payments/Payments.tsx`)

#### ✅ Задача 8: Django Admin для управления платформой
**Реализована расширенная админ-панель с модерацией:**
1. **CustomUserAdmin** - Управление пользователями
2. **TaskAdmin** - Управление заданиями с модерацией
3. **TransactionAdmin** - Управление транзакциями и выплатами

#### ✅ Задача 9: Модульное тестирование (Backend)
**Покрыты тестами критические модули системы:**
1. **Пользователи** (`backend/tests/test_users.py`): регистрация, вход, профиль, JWT, роли.
2. **Задания** (`backend/tests/test_tasks.py`): создание, статусы, права доступа, API.
3. **Платежи** (`backend/tests/test_payments.py`): кошельки, транзакции, пополнение, выплаты.

---

#### ✅ Предыдущие задачи:
**Задача 3: Генерация PDF документов (Backend)**
**Задача 2: CRUD для заданий (Backend)**
**Задача 1: Пользователи и роли (Backend)**

---

## Запуск проекта

### 🐳 Запуск через Docker (рекомендуется)

Самый быстрый способ запустить весь проект (Backend, Frontend, Database, Redis):

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/nickolaa/konsol-pro-clone.git
   cd konsol-pro-clone
   ```

2. **Настройте переменные окружения:**
   Скопируйте пример файла конфигурации:
   ```bash
   cp .env.example .env
   ```

3. **Запустите контейнеры:**
   ```bash
   docker-compose up --build
   ```

4. **Выполните миграции и создайте суперпользователя (в новом терминале):**
   ```bash
   docker-compose exec backend python manage.py migrate
   docker-compose exec backend python manage.py createsuperuser
   ```

5. **Проект будет доступен по адресам:**
   - **Frontend:** http://localhost:3000
   - **Backend API:** http://localhost:8000/api/
   - **Django Admin:** http://localhost:8000/admin/

---

### Локальный запуск (без Docker)

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## Тестирование

### Запуск тестов Backend
```bash
# В Docker:
docker-compose exec backend python manage.py test

# Локально:
cd backend
python manage.py test
```

---

## Технологический стек

### Backend
- Python 3.11+, Django 4.2+, DRF 3.14+
- PostgreSQL, Redis, Celery
- JWT (SimpleJWT), WeasyPrint (PDF)

### Frontend
- React 18.2.0, TypeScript 5.3.3
- Redux Toolkit 2.0.1, React Router DOM 6.21.1
- Axios, Material-UI / Tailwind

---

## Лицензия
MIT License

## Контакты
Для вопросов и предложений: [ваш email]
