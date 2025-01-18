import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_phone_number(value):
    """
    Валидатор для номера телефона
    """
    if not re.match(r'^\+?[\d\s-()]+$', value):
        raise ValidationError(
            _('%(value)s не является корректным номером телефона'),
            params={'value': value},
        )

def validate_cyrillic_name(value):
    """
    Валидатор для имен на кириллице
    """
    if not re.match(r'^[А-ЯЁа-яё\s-]+$', value):
        raise ValidationError(
            _('%(value)s должно содержать только кириллические буквы'),
            params={'value': value},
        )

def validate_inn(value):
    """
    Валидатор для ИНН
    """
    if not isinstance(value, str):
        value = str(value)
    if not value.isdigit():
        raise ValidationError(_('ИНН должен содержать только цифры'))

    if len(value) not in (10, 12):
        raise ValidationError(_('ИНН должен содержать 10 или 12 цифр'))

    def inn_csum(inn, coefficients):
        return str(sum(c * int(i) for c, i in zip(coefficients, inn)) % 11 % 10)

    if len(value) == 10:
        if value[-1] != inn_csum(value[:-1], (2, 4, 10, 3, 5, 9, 4, 6, 8)):
            raise ValidationError(_('Неверный ИНН'))
    else:
        if (value[-2] != inn_csum(value[:-2], (7, 2, 4, 10, 3, 5, 9, 4, 6, 8)) or
            value[-1] != inn_csum(value[:-1], (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8))):
            raise ValidationError(_('Неверный ИНН'))

def validate_file_extension(value, allowed_extensions):
    """
    Валидатор для расширения файла
    """
    ext = value.name.split('.')[-1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(
            _('Неподдерживаемый тип файла. Разрешены: %(extensions)s'),
            params={'extensions': ', '.join(allowed_extensions)},
        )

def validate_file_size(value, max_size_mb):
    """
    Валидатор для размера файла
    """
    if value.size > max_size_mb * 1024 * 1024:
        raise ValidationError(
            _('Размер файла не должен превышать %(size)d МБ'),
            params={'size': max_size_mb},
        )