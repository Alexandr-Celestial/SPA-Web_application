# 30.1 Вьюсеты и дженерики

Проект представляет собой учебный API на Django с использованием Django REST Framework (DRF).

## Стек

- Python 3.x
- Django 4.x (или ваша версия)
- Django REST Framework
- PostgreSQL (в качестве базы данных)
- (Дополнительно) Pillow для обработки изображений

## Описание проекта

- Кастомная модель пользователя с авторизацией по email  
- Приложение `users` — кастомный пользователь с полями email, телефон, город и аватарка  
- Приложение `lms` (или `materials`) — модели `Course` и `Lesson`  
- Связь: один курс содержит множество уроков  
- CRUD для курсов реализован через ViewSet  
- CRUD для уроков реализован через generic-классы (ListCreate, RetrieveUpdateDestroy)  
- Тестирование API — при помощи Postman

# 30.2 Сериализаторы

## Задание 1  
### Добавление в сериализатор модели Course поля количества уроков

- В сериализаторе модели `Course` добавлено поле `number_of_lessons` с помощью `SerializerMethodField`.
- Реализован метод `get_number_of_lessons`, который возвращает количество связанных уроков курса.
- Пример реализации в `CourseSerializer`:

```
number_of_lessons = serializers.SerializerMethodField()

def get_number_of_lessons(self, instance):
return instance.lesson_set.count()
```

## Задание 2  
### Создание модели Платежи (Payments) в приложении users

- Создана модель `Payments` со следующими полями:
- `user` — внешняя связь (ForeignKey) на модель пользователя `User`
- `payment_date` — дата и время оплаты (`DateTimeField`)
- `paid_course` — внешняя связь на модель курса `Course`, может быть `null`
- `paid_lesson` — внешняя связь на модель урока `Lesson`, может быть `null`
- `payment_amount` — сумма оплаты (`PositiveIntegerField`)
- `payment_method` — способ оплаты (`CharField` с вариантами: наличные, перевод на счет)
- Выполнены миграции.
- Для наполнения данных использовалась кастомная management-команда, которая создает пользователей, курсы, уроки и платежи.

---

## Задание 3  
### Вывод количества уроков и подробной информации по урокам в сериализаторе Course

- Создан вложенный сериализатор `LessonSerializer` для модели `Lesson`.
- В `CourseSerializer` добавлены два поля:
- `lessons` — список сериализованных уроков (используется `LessonSerializer(many=True, read_only=True, source='lesson_set')`)
- `number_of_lessons` — количество уроков через `SerializerMethodField`
- В результате сериализатор одновременно возвращает и количество уроков, и их подробную информацию.

## Задание 4  
### Настройка фильтрации и сортировки для API списка платежей

- Создан контроллер `PaymentsListAPIView` на основе `generics.ListAPIView`.
- Подключены фильтрация и сортировка:
- `DjangoFilterBackend` для фильтрации по курсу, уроку и способу оплаты.
- `OrderingFilter` для сортировки по дате оплаты.
- В `filterset_fields` указаны поля:
- `paid_course`
- `paid_lesson`
- `payment_method`
- В `ordering_fields` добавлено:
- `payment_date`
- Сортировка по умолчанию — по дате оплаты по убыванию (`-payment_date`).
- Для работы подключен и настроен пакет `django-filter` в `settings.py`.