from datetime import datetime

from django.core.management import BaseCommand

from materials.models import Course, Lesson
from users.models import Payments, User


class Command(BaseCommand):
    help = 'Добавляет платежи'

    def handle(self, *args, **options):
        user_2, _ = User.objects.get_or_create(email='user2@mail.ru', defaults={'is_active': True})
        user_3, _ = User.objects.get_or_create(email='user3@mail.ru', defaults={'is_active': True})
        user_4, _ = User.objects.get_or_create(email='user4@mail.ru', defaults={'is_active': True})

        course_web, _ = Course.objects.get_or_create(title='веб-разработчик', defaults={'description': 'Описание веб-разработчика'})
        course_python, _ = Course.objects.get_or_create(title='python-разработчик', defaults={'description': 'Описание python-разработчика'})
        qr_engineer, _ = Course.objects.get_or_create(title='тестировщик', defaults={'description': 'Описание тестировщика'})

        lesson_2, _ = Lesson.objects.get_or_create(
            title='урок №2',
            defaults={'course': course_web, 'description': 'Описание урока №2'}
        )
        lesson_3, _ = Lesson.objects.get_or_create(
            title='урок №3',
            defaults={'course': course_python, 'description': 'Описание урока №3'}
        )
        lesson_4, _ = Lesson.objects.get_or_create(
            title='урок №4',
            defaults={'course': qr_engineer, 'description': 'Описание урока №4'}
        )

        Payments.objects.create(
            user=user_2,
            payment_date=datetime(2025, 2, 2),
            paid_course=course_web,
            paid_lesson=lesson_2,
            payment_amount=20000,
            payment_method='cash'  # или 'transfer', согласно choices
        )

        Payments.objects.create(
            user=user_3,
            payment_date=datetime(2025, 2, 2),
            paid_course=course_python,
            paid_lesson=lesson_3,
            payment_amount=20000,
            payment_method='transfer'
        )

        Payments.objects.create(
            user=user_4,
            payment_date=datetime(2025, 2, 2),
            paid_course=qr_engineer,
            paid_lesson=lesson_4,
            payment_amount=20000,
            payment_method='cash'
        )

        self.stdout.write(self.style.SUCCESS('Платежи успешно добавлены'))
