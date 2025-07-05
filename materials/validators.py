from rest_framework.serializers import ValidationError


def youtube_url_validator(value):
    """
    Валидатор: разрешает только ссылки, начинающиеся на https://www.youtube.com/
    """
    if not value.startswith("https://www.youtube.com/"):
        raise ValidationError("Допустимы только ссылки на YouTube!")
