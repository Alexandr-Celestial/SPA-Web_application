from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Создаёт суперпользователя'

    def handle(self, *args, **options):
        super_user: User = User.objects.create(email='admin@admin.ru', is_staff=True, is_active=True, is_superuser=True)
        super_user.set_password('1234')
        super_user.save()
        self.stdout.write(self.style.SUCCESS('Суперпользователь успешно добавлен'))