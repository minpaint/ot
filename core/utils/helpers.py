from datetime import datetime, timedelta
import calendar

def get_month_range(date=None):
    """
    Возвращает начало и конец месяца для заданной даты
    """
    if date is None:
        date = datetime.now()

    first_day = date.replace(day=1)
    last_day = date.replace(
        day=calendar.monthrange(date.year, date.month)[1],
        hour=23, minute=59, second=59
    )
    return first_day, last_day

def get_age(birth_date):
    """
    Вычисляет возраст по дате рождения
    """
    today = datetime.now()
    age = today.year - birth_date.year
    if today.month < birth_date.month or (
        today.month == birth_date.month and 
        today.day < birth_date.day
    ):
        age -= 1
    return age

def format_duration(seconds):
    """
    Форматирует продолжительность из секунд в читаемый формат
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

    parts = []
    if days > 0:
        parts.append(f"{days}д")
    if hours > 0:
        parts.append(f"{hours}ч")
    if minutes > 0:
        parts.append(f"{minutes}м")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}с")

    return " ".join(parts)

def get_quarter_dates(year, quarter):
    """
    Возвращает начало и конец квартала
    """
    first_month = 3 * quarter - 2
    last_month = 3 * quarter

    start_date = datetime(year, first_month, 1)
    end_date = datetime(
        year, 
        last_month, 
        calendar.monthrange(year, last_month)[1],
        23, 59, 59
    )

    return start_date, end_date

def humanize_size(size_bytes):
    """
    Преобразует размер в байтах в человекочитаемый формат
    """
    for unit in ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} ПБ"