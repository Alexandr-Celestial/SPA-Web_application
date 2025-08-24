from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from users.models import Payments
from materials.models import Course, Lesson
from decimal import Decimal


class Command(BaseCommand):
    """ Заполнение БД необходимыми данными для проверки. """

    help = ' Заполнение БД необходимыми данными для проверки. '

    def handle(self, *args, **options):
        user_model = get_user_model()

        superuser = user_model.objects.create(
            email="admin@admin.com",
            username = "admin",
            first_name = "Super",
            last_name = "User",
            phone_number = "+77777777777",
            is_active = True,
            is_staff = True,
            is_superuser = True
        )
        superuser.set_password("123456")
        superuser.save()
        self.stdout.write("Суперпользователь успешно добавлен!")

        simple_user = user_model.objects.create(
            email="user @ example.com",
            username = "user",
            first_name = "Simple",
            last_name = "User",
            phone_number = "+75555555555",
            is_active = True,
            is_staff = False,
            is_superuser = False
        )
        simple_user.set_password("654321")
        simple_user.save()
        self.stdout.write("Обычный пользователь успешно добавлен!")

        course_for_superuser = Course.objects.create(
            name="Python Basics",
            description="Основы Python.",
            owner=superuser
        )
        self.stdout.write(f"Курс '{course_for_superuser.name}' успешно создан.")

        course_for_simple_user = Course.objects.create(
            name="HTML & CSS",
            description="Базовые знания HTML и CSS.",
            owner=simple_user
        )
        self.stdout.write(f"Курс '{course_for_simple_user.name}' успешно создан.")

        lesson_for_superuser = Lesson.objects.create(
            name="Base func",
            description="Начало изучения функций в Python.",
            owner=superuser,
            course=course_for_superuser
        )
        self.stdout.write(f"Урок '{lesson_for_superuser.name}' успешно создан!")

        lesson_for_simple_user = Lesson.objects.create(
            name="Basic in HTML",
            description="Основные теги HTML.",
            owner=simple_user,
            course=course_for_simple_user
        )
        self.stdout.write(f"Урок '{lesson_for_simple_user.name}' успешно создан!")

        payment_for_superuser = Payments.objects.create(
            name="PAY-ID-38847",
            user=superuser,
            course=course_for_superuser,
            lesson=lesson_for_superuser,
            payment_day=now(),
            amount=Decimal('2254.00'),
            payment_method='transfer'
        )
        self.stdout.write(f"Платеж № {payment_for_superuser.id} для суперпользователя успешно добавлен!")

        payment_for_simple = Payments.objects.create(
            name="PAY-ID-68767",
            user=simple_user,
            course=course_for_simple_user,
            lesson=lesson_for_simple_user,
            payment_day=now(),
            amount=Decimal('1789.00'),
            payment_method='cash'
        )
        self.stdout.write(f"Платеж № {payment_for_simple.id} для простого пользователя успешно добавлен!")
