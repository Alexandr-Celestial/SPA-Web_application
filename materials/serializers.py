from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import LintToVideoYTValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Lesson"""

    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=False, allow_null=True)
    link_to_video = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'course', 'link_to_video']
        # validators = [LintToVideoYTValidator(field='link_to_video')]

    def validate_link_to_video(self, value):
        validator = LintToVideoYTValidator(field='link_to_video')
        validator(value)
        return value

class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Course"""

    number_of_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['title', 'description', 'number_of_lessons', 'lessons', 'is_subscribed']

    def get_number_of_lessons(self, instance):
        return instance.lesson_set.count()

    def get_is_subscribed(self, instance):
        user = self.context.get('request').user
        return instance.subscriptions.filter(user=user).exists()
