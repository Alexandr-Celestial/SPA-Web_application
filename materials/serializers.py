from rest_framework import serializers

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Course"""
    class Meta:
        model = Course
        fields = ['title', 'description']

class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Lesson"""

    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Lesson
        fields = ['title', 'description', 'course']
