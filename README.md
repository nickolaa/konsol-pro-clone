# konsol-pro-clone
Платформа для работы с самозанятыми - аналог Консоль.Про. Автоматизация заданий, документооборота и выплат.

## Текущий статус

### Реализовано

#### ✅ Задача 4: Авторизация и регистрация пользователей (Frontend)

**Создана полная система авторизации на frontend:**

1. **Redux Store для авторизации** (`frontend/src/features/auth/authSlice.ts`)
   - Управление состоянием пользователя (isAuthenticated, user, loading, error)
   - Асинхронные thunk actions для login и register
   - Интеграция с API через axios
   - Сохранение токена в localStorage

2. **Страница входа** (`frontend/src/pages/auth/Login.tsx`)
   - Форма входа с полями email и password
   - Валидация на стороне клиента
   - Обработка ошибок и состояния загрузки
   - Перенаправление после успешного входа
   - Ссылка на страницу регистрации

3. **Страница регистрации** (`frontend/src/pages/auth/Register.tsx`)
   - Форма регистрации с полями: email, имя, фамилия, пароль, подтверждение пароля
   - Выбор типа пользователя (Заказчик/Исполнитель)
   - Валидация паролей (минимум 8 символов, совпадение)
   - Обработка ошибок и состояния загрузки
   - Перенаправление после успешной регистрации

4. **Маршрутизация** (`frontend/src/routes.tsx`)
   - Настроены публичные маршруты: `/`, `/login`, `/register`
   - Защищенный маршрут `/dashboard` с компонентом ProtectedRoute
   - Автоматическое перенаправление неавторизованных пользователей на /login
   - Placeholder компоненты для Home и Dashboard

**Использованные технологии:**
- React 18.2.0
- Redux Toolkit 2.0.1
- React Router DOM 6.21.1
- TypeScript 5.3.3
- Axios 1.6.3

---

#### ✅ Предыдущие задачи:

**Задача 3: Генерация PDF документов (Backend)**
- Модели Contract, Act, ContractTemplate, Signature
- ViewSets для работы с контрактами и актами
- Генерация PDF из шаблонов с подстановкой данных
- Загрузка готовых PDF файлов
- Цифровая подпись документов

**Задача 2: CRUD для заданий (Backend)**
- Модели Task и TaskTemplate
- API endpoints для создания, редактирования, публикации заданий
- Система статусов заданий
- Связь заданий с пользователями и шаблонами

**Задача 1: Пользователи и роли (Backend)**
- Кастомная модель User с полями для заказчиков и исполнителей
- JWT аутентификация через rest_framework_simplejwt
- API endpoints: регистрация, вход, получение профиля
- Разделение прав доступа по ролям

---

## Следующие шаги

### Задача 5: Интеграция Frontend с Backend API
- Настройка CORS для взаимодействия frontend и backend
- Тестирование авторизации и регистрации
- Реализация обновления токена
- Создание интерцепторов для автоматической подстановки токена

### Задача 6: Страница заданий (Frontend)
- Список заданий с фильтрацией и поиском
- Создание нового задания
- Редактирование задания
- Просмотр деталей задания

### Задача 7: Страница документов (Frontend)
- Просмотр контрактов и актов
- Загрузка PDF документов
- Подписание документов

### Задача 8: Дашборд и статистика
- Панель управления для заказчиков
- Панель управления для исполнителей
- Графики и аналитика

---

## Структура проекта

```
konsol-pro-clone/
├── backend/                 # Django backend
│   ├── users/              # Модуль пользователей
│   ├── tasks/              # Модуль заданий
│   └── contracts/          # Модуль документов
├── frontend/               # React frontend
│   ├── src/
│   │   ├── app/           # Redux store
│   │   ├── features/      # Redux slices
│   │   │   └── auth/      # Авторизация
│   │   ├── pages/         # Страницы
│   │   │   └── auth/      # Login, Register
│   │   ├── utils/         # API конфигурация
│   │   ├── App.tsx        # Главный компонент
│   │   └── routes.tsx     # Маршрутизация
│   └── package.json
├── config/                 # Конфигурация проекта
├── docker-compose.yml
└── README.md
```

## Установка и запуск

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### Docker
```bash
docker-compose up --build
```

## API Endpoints

### Авторизация
- `POST /api/users/register/` - Регистрация
- `POST /api/users/login/` - Вход
- `GET /api/users/profile/` - Профиль пользователя
- `POST /api/token/refresh/` - Обновление токена

### Задания
- `GET /api/tasks/` - Список заданий
- `POST /api/tasks/` - Создать задание
- `GET /api/tasks/{id}/` - Детали задания
- `PUT /api/tasks/{id}/` - Обновить задание
- `POST /api/tasks/{id}/publish/` - Опубликовать задание

### Документы
- `GET /api/contracts/` - Список контрактов
- `POST /api/contracts/` - Создать контракт
- `GET /api/contracts/{id}/download_pdf/` - Скачать PDF
- `POST /api/contracts/{id}/sign/` - Подписать документ

## Стек технологий

### Backend
- Python 3.11
- Django 5.0
- Django REST Framework
- PostgreSQL
- ReportLab (PDF генерация)
- JWT Authentication

### Frontend
- React 18.2
- TypeScript 5.3
- Redux Toolkit 2.0
- React Router 6.21
- Axios 1.6
- Vite 3.5

### DevOps
- Docker
- Docker Compose
- Nginx
