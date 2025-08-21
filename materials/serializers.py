from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Lesson"""

    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Lesson
        fields = ['title', 'description', 'course']

class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Course"""

    number_of_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')

    class Meta:
        model = Course
        fields = ['title', 'description', 'number_of_lessons', 'lessons']

    def get_number_of_lessons(self, instance):
        return instance.lesson_set.count()
