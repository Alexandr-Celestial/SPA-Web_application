from celery import shared_task
from django.core.mail import send_mail
from users.models import Subscription
from materials.models import Course

@shared_task
def send_course_update_mail(course_id):
    course: Course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course).select_related('user')

    recipients = [subscription.user.email for subscription in subscriptions if subscription.user.email]

    if not recipients:
        return

    send_mail(
        subject=f"Обновления в курсе {course.title}",
        message=f"В курсе '{course.title}' появились новые материалы. Заходите и смотрите!",
        from_email='user111y@mail.com',  # Замените на вашу почту
        recipient_list=recipients,
        fail_silently=False,
    )