from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskViewSet,
    TaskTemplateViewSet,
    DocumentViewSet,
    PaymentViewSet,
    TransactionViewSet,
    ReviewViewSet
)

# Создаем router для автоматической генерации URL
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'task-templates', TaskTemplateViewSet, basename='task-template')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]

# Доступные API endpoints:
# GET   /api/tasks/            - Список заданий
# POST  /api/tasks/            - Создать задание (черновик)
# GET   /api/tasks/{id}/       - Детали задания
# PUT   /api/tasks/{id}/       - Обновить задание
# PATCH /api/tasks/{id}/       - Частично обновить задание
# DELETE /api/tasks/{id}/      - Удалить задание
# POST  /api/tasks/{id}/publish/  - Опубликовать задание
# POST  /api/tasks/{id}/assign/   - Взять задание в работу
# POST  /api/tasks/{id}/complete/ - Завершить задание
#
# GET   /api/task-templates/   - Список шаблонов
# POST  /api/task-templates/   - Создать шаблон
# GET   /api/task-templates/{id}/ - Детали шаблона
# PUT   /api/task-templates/{id}/ - Обновить шаблон
# DELETE /api/task-templates/{id}/ - Удалить шаблон
#
# GET   /api/documents/        - Список документов
# GET   /api/documents/{id}/   - Детали документа
#
# GET   /api/payments/         - Список выплат
# GET   /api/payments/{id}/    - Детали выплаты
#
# GET   /api/transactions/     - История транзакций
#
# GET   /api/reviews/          - Список отзывов
# POST  /api/reviews/          - Оставить отзыв
