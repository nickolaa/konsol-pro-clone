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

#### ✅ Задача 6: Лента заданий для исполнителей (Frontend)

**Реализована полная система ленты заданий:**

1. **Redux Store для заданий** (`frontend/src/features/tasks/tasksSlice.ts`)
   - Управление состоянием заданий (tasks, loading, error)
   - Async thunk action для fetchTasks
   - Интеграция с API через axios
   - Типизация Task interface

2. **Страница TaskFeed** (`frontend/src/pages/tasks/TaskFeed.tsx`)
   - Лента всех опубликованных заданий
   - Фильтрация по названию, категории и бюджету
   - Отображение списка заданий через TaskCard компонент
   - Обработка состояний загрузки и ошибок

3. **Страница MyTasks** (`frontend/src/pages/tasks/MyTasks.tsx`)
   - Отображение активных заданий исполнителя
   - Фильтрация по executor_id и статусу in_progress
   - Защищённый маршрут (требуется авторизация)

4. **Страница TaskHistory** (`frontend/src/pages/tasks/TaskHistory.tsx`)
   - История завершённых заданий
   - Фильтрация по статусу completed
   - Отображение бейджа "Завершено"
   - Защищённый маршрут

5. **Компонент TaskCard** (`frontend/src/components/TaskCard.tsx`)
   - Карточка задания с основной информацией
   - Отображение: заголовок, описание, бюджет, категория, дедлайн
   - Ссылка на детальную страницу задания
   - Русская локализация

6. **Маршрутизация** (`frontend/src/routes.tsx`)
   - Добавлены маршруты:
     - `/tasks` → TaskFeed (публичный)
     - `/my-tasks` → MyTasks (защищённый)
     - `/task-history` → TaskHistory (защищённый)
   - Интеграция с ProtectedRoute wrapper

**Результат:** Полнофункциональный UI для просмотра ленты заданий, управления активными заданиями и просмотра истории для исполнителей.


#### ✅ Задача 7: Интерфейс пополнения баланса и выплат (Backend + Frontend)

**Реализована базовая система платежей и транзакций:**

1. **Модель Transaction** (`backend/models.py`)
   - Типы транзакций: deposit (пополнение), payout (выплата), payment (оплата задания)
   - Статусы: pending, completed, failed
   - Связь с пользователем и заданием
   - Поля: amount, description, created_at, processed_at

2. **TransactionSerializer** (`backend/serializers.py`)
   - Сериализация транзакций с UserSerializer
   - Display поля для transaction_type и status
   - Read-only поля: id, user, created_at, processed_at

3. **Redux Store для платежей** (`frontend/src/features/payments/paymentsSlice.ts`)
   - Управление состоянием: transactions, balance, loading, error
   - Async thunks:
     - fetchTransactions - получение истории транзакций
     - createDeposit - создание пополнения баланса
     - requestPayout - запрос на выплату
   - Типизация Transaction interface

**Результат:** Фундамент для системы платежей - модели данных, сериализаторы и Redux инфраструктура для управления транзакциями, пополнениями баланса и 


#### ✅ Задача 8: Django Admin для управления платформой

**Реализована расширенная админ-панель с модерацией:**

1. **CustomUserAdmin** - Управление пользователями
   - Фильтры: is_freelancer, is_employer, is_active, is_staff, date_joined
   - Поиск: email, phone, telegram_id
   - Действия: активация/деактивация пользователей
   - Группировка полей: личная информация, роли, права доступа, даты
   - Сортировка по дате регистрации (новые первыми)

2. **TaskAdmin** - Управление заданиями с модерацией
   - Цветные бейджи статусов (draft, published, in_progress, completed, cancelled)
   - Фильтры: status, created_at, updated_at
   - Поиск: title, description, employer__email, freelancer__email
   - Иерархия по датам (date_hierarchy)
   - Действия модерации:
     - Одобрить задания (draft → published)
     - Отклонить задания (cancelled)
     - Перевести в работу (in_progress)
     - Завершить задания (completed)

3. **TransactionAdmin** - Управление транзакциями и выплатами
   - Цветные бейджи типов (deposit, payout, payment)
   - Цветные бейджи статусов (pending, completed, failed)
   - Фильтры: transaction_type, status, created_at
   - Поиск: user__email, description
   - Действия:
     - Одобрить транзакции (pending → completed)
     - Отклонить транзакции (pending → failed)
   - Автоматическое проставление processed_at

4. **Дополнительные админки:**
   - TaskTemplateAdmin - шаблоны заданий
   - DocumentAdmin - документы с фильтрацией по типам
   - PaymentAdmin - платежи с фильтрами статусов
   - ContractAdmin, ActAdmin - договоры и акты
   - SignatureAdmin - цифровые подписи

**Результат:** Полнофункциональная админ-панель Django с фильтрами, поиском, цветными индикаторами и действиями массовой модерации для управления всеми сущностями платформы.выплатами.


#### ✅ Задача 5: Дашборд компании (Frontend)

**Реализован функциональный дашборд для компаний:**

1. **CompanyDashboard** (`frontend/src/pages/company/CompanyDashboard.tsx`)
   - Обзорная страница с ключевыми метриками
   - Статистика по заданиям (всего, активные, завершенные)
   - Статистика по бюджету и расходам
   - Список последних заданий
   - Быстрый доступ к созданию нового задания

2. **TaskManagement** (`frontend/src/pages/company/TaskManagement.tsx`)
   - Полный список заданий компании
   - Фильтры по статусу (draft, published, in_progress, completed, cancelled)
   - Действия с заданиями:
     - Создание нового задания
     - Редактирование черновиков
     - Публикация заданий
     - Отмена заданий
     - Просмотр откликов
   - Таблица с сортировкой по датам и статусам

3. **CreateTask** (`frontend/src/pages/company/CreateTask.tsx`)
   - Форма создания задания с полями:
     - Название и описание
     - Категория
     - Бюджет (фиксированный/диапазон)
     - Крайний срок
     - Требуемые навыки
   - Выбор шаблона задания (опционально)
   - Сохранение как черновик или сразу публикация
   - Валидация полей на стороне клиента

4. **EditTask** (`frontend/src/pages/company/EditTask.tsx`)
   - Редактирование существующего задания
   - Загрузка данных задания по ID
   - Те же поля что и при создании
   - Возможность изменить статус
   - Предпросмотр изменений

**Результат:** Полнофункциональная панель управления для компаний с возможностью создания, редактирования и управления заданиями.

---

#### ✅ Задача 7: Интерфейс пополнения баланса и выплат (Backend + Frontend)

**Реализована базовая система платежей и транзакций:**

1. **Модель Transaction** (`backend/models.py`)
   - Типы транзакций: deposit (пополнение), payout (выплата), payment (оплата задания)
   - Статусы: pending, completed, failed
   - Связь с пользователем и заданием
   - Поля: amount, description, created_at, processed_at

2. **TransactionSerializer** (`backend/serializers.py`)
   - Сериализация транзакций с UserSerializer
   - Display поля для transaction_type и status
   - Read-only поля: id, user, created_at, processed_at

3. **Redux Store для платежей** (`frontend/src/features/payments/paymentsSlice.ts`)
   - Управление состоянием: transactions, balance, loading, error
   - Async thunks:
     - fetchTransactions – получение истории транзакций
     - createDeposit – создание пополнения баланса
     - requestPayout – запрос на выплату
   - Типизация Transaction interface

4. **Страница Payments** (`frontend/src/pages/payments/Payments.tsx`)
   - Отображение текущего баланса
   - Кнопки для пополнения и вывода средств
   - История транзакций в табличном виде
   - Фильтрация по типу транзакции
   - Цветные бейджи для статусов

5. **Компонент DepositModal**
   - Модальное окно для пополнения баланса
   - Выбор суммы или ввод произвольной
   - Выбор способа оплаты (карта, электронный кошелек)
   - Интеграция с платежной системой (заглушка)

6. **Компонент PayoutModal**
   - Модальное окно для запроса выплаты
   - Ввод суммы с валидацией (не больше баланса)
   - Выбор метода получения (банковский счет, карта)
   - Информация о сроках обработки

**Результат:** Фундамент для системы платежей – модели данных, сериализаторы и Redux инфраструктура для управления транзакциями, пополнениями баланса и выплатами.

---

## Следующие шаги

### Задача 8: Админ-панель Django (Backend)

- Настройка Django Admin для всех моделей
- Кастомные админки для User, Task, Transaction
- Фильтры и поиск
- Массовые действия
- Экспорт данных

### Задача 9: Система откликов и выбора исполнителя

- Модель Response (отклик на задание)
- API для создания откликов
- Просмотр откликов работодателем
- Выбор исполнителя и начало работы
- Уведомления об откликах

### Задача 10: Интеграция платежной системы

- Подключение реального платежного провайдера (ЮКасса, Stripe)
- Webhooks для обработки платежей
- Автоматическое обновление баланса
- Безопасное хранение платежных данных
- Возврат средств при отмене

### Задача 11: Система уведомлений

- Push-уведомления в браузере
- Email уведомления
- Уведомления о новых заданиях
- Уведомления об откликах
- Уведомления о платежах

### Задача 12: Чат между заказчиком и исполнителем

- WebSocket соединение для реального времени
- Модель Message
- Интерфейс чата
- Отправка файлов
- История сообщений

---

## Технологический стек

### Backend
- Python 3.11+
- Django 4.2+
- Django REST Framework 3.14+
- PostgreSQL 15+
- Redis (для кэширования и очередей)
- Celery (для фоновых задач)
- JWT аутентификация (rest_framework_simplejwt)
- WeasyPrint (генерация PDF)

### Frontend
- React 18.2.0
- TypeScript 5.3.3
- Redux Toolkit 2.0.1
- React Router DOM 6.21.1
- Axios 1.6.3
- Material-UI или Tailwind CSS
- React Hook Form (формы)
- Yup (валидация)

### DevOps
- Docker & Docker Compose
- Nginx (reverse proxy)
- GitHub Actions (CI/CD)
- Gunicorn (WSGI сервер)

---

## Архитектура проекта

```
konsol-pro-clone/
├── backend/
│   ├── users/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── tasks/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── contracts/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── utils/
│   │       └── pdf_generator.py
│   ├── payments/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   └── views.py
│   └── config/
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── auth/
│   │   │   └── tasks/
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   │   └── authSlice.ts
│   │   │   ├── tasks/
│   │   │   │   └── tasksSlice.ts
│   │   │   └── payments/
│   │   │       └── paymentsSlice.ts
│   │   ├── pages/
│   │   │   ├── auth/
│   │   │   ├── tasks/
│   │   │   ├── company/
│   │   │   └── payments/
│   │   ├── store/
│   │   │   └── index.ts
│   │   ├── api/
│   │   │   └── axios.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   └── package.json
├── docker-compose.yml
└── README.md
```

---

## Запуск проекта

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker

```bash
docker-compose up --build
```

---

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Регистрация
- `POST /api/auth/login/` - Вход (получение токенов)
- `POST /api/auth/token/refresh/` - Обновление токена
- `GET /api/auth/profile/` - Получение профиля
- `PUT /api/auth/profile/` - Обновление профиля

### Tasks
- `GET /api/tasks/` - Список заданий
- `POST /api/tasks/` - Создание задания
- `GET /api/tasks/{id}/` - Детали задания
- `PUT /api/tasks/{id}/` - Обновление задания
- `DELETE /api/tasks/{id}/` - Удаление задания
- `POST /api/tasks/{id}/publish/` - Публикация задания
- `POST /api/tasks/{id}/cancel/` - Отмена задания

### Contracts
- `GET /api/contracts/` - Список договоров
- `POST /api/contracts/` - Создание договора
- `GET /api/contracts/{id}/download/` - Скачать PDF
- `POST /api/contracts/{id}/sign/` - Подписать договор

### Payments
- `GET /api/transactions/` - История транзакций
- `POST /api/transactions/deposit/` - Пополнение баланса
- `POST /api/transactions/payout/` - Запрос выплаты
- `GET /api/balance/` - Текущий баланс

---

## Безопасность

- JWT токены с коротким временем жизни
- HTTPS обязателен в production
- CORS настроен для фронтенда
- Валидация данных на backend и frontend
- Защита от CSRF атак
- Rate limiting для API
- Хеширование паролей (Django по умолчанию)
- Безопасное хранение токенов в localStorage

---

## Тестирование

### Backend
```bash
python manage.py test
```

### Frontend
```bash
npm run test
```

---

## Лицензия

MIT License

---

## Контакты

Для вопросов и предложений: [ваш email]
