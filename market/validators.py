from django.core.exceptions import ValidationError


def validate_price(value):
    if value < 0:
        raise ValidationError(
            'Price can\'t be less than 0',
            params={'value': value}
        )