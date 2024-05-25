from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from ..models import EmailSuffixFormat

# VALIDATOR


def validate_email_suffix_format(value):
    """
    Validate the email suffix format, check if the email suffix is in the whitelist
    Note: This function will raise a ValidationError if the email suffix is not in the whitelist
    Must be used with the transaction.atomic() context manager
    """
    message = "请提供有效的电子邮件, 请检查有效的电子邮件格式"
    code = "invalid_email_suffix_format"
    try:
        validate_email(value)
    except ValidationError:
        raise ValidationError(message, code=code, params={"value": value})

    _, suffix = value.rsplit("@", 1)

    suffix_formats = EmailSuffixFormat.objects.select_for_update().filter(
        is_active=True
    )
    for suffix_format in suffix_formats:
        if suffix_format.format == "@*" or suffix.startswith(suffix_format.format[1:]):
            return
    raise ValidationError(message, code=code, params={"value": value})
