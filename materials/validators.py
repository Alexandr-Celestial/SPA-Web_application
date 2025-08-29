from rest_framework.serializers import ValidationError

class LintToVideoYTValidator:
    """Осуществляет проверку на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com"""

    VALID_URL = 'youtube.com'

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        print(f"Validating link_to_video: {value}")
        if self.VALID_URL not in value:
            raise ValidationError("Ссылка должна вести на ресурсы: 'youtube.com'")
