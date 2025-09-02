from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CASCADE

# from materials.models import Course, Lesson


class User(AbstractUser):
    """Модель пользователя"""

    username = None

    email = models.EmailField(unique=True, null=False, verbose_name='email', help_text='Введите адрес эл.почты')
    avatar = models.ImageField(upload_to='avatar/', verbose_name='аватар', null=True, blank=True)
    phone_number = models.CharField(max_length=30, verbose_name='номер телефона', null=True, blank=True)
    city = models.CharField(max_length=100, verbose_name='город', null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    """Модель платежи"""

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'наличные'),
        ('transfer', 'перевод на счет'),
    ]

    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=CASCADE)
    payment_date = models.DateTimeField(verbose_name='дата оплаты', null=True, blank=True)
    session_id = models.TextField(verbose_name='id сессии', null=True, blank=True)
    link = models.TextField(verbose_name='Ссылка на оплату', null=True, blank=True)
    paid_course = models.ForeignKey('materials.Course', verbose_name='оплаченный курс', on_delete=CASCADE, null=True, blank=True)
    paid_lesson = models.ForeignKey('materials.Lesson', verbose_name='оплаченный урок', on_delete=CASCADE, null=True, blank=True)
    payment_amount = models.PositiveIntegerField(verbose_name='сумма оплаты', null=True, blank=True)
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES, verbose_name='способ оплаты',
                                      null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.payment_amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Subscription(models.Model):
    """Модель подписки"""

    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=CASCADE, null=True, blank=True)
    course = models.ForeignKey('materials.Course', verbose_name="Курс", on_delete=CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Подписка пользователя {self.user} на курс {self.course}"

    class Meta:
        verbose_name = "подписка"
        verbose_name_plural = "подписки"
