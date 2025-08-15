from django.db import models
from django.db.models import RESTRICT


class Course(models.Model):
    """Класс курса"""

    title = models.CharField(max_length=150, null=False, verbose_name="Название")
    preview = models.ImageField(max_length=150, upload_to="media/",verbose_name="превью")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"

class Lesson(models.Model):
    title = models.CharField(max_length=150, null=False, verbose_name="Название", unique=True)
    preview = models.ImageField(max_length=150, upload_to="media/", verbose_name="превью")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    link_to_video = models.URLField(null=True, blank=True, verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, verbose_name="Курс" ,on_delete=RESTRICT, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"