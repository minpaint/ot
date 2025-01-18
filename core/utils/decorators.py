import time
import logging
from functools import wraps
from django.db import transaction
from django.core.cache import cache
from django.conf import settings

def retry_on_error(max_attempts=3, delay=1):
    """
    Декоратор для повторных попыток выполнения функции при ошибке
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def cache_result(timeout=300):
    """
    Декоратор для кэширования результатов функции
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not settings.DEBUG:  # Не используем кэш в режиме отладки
                cache_key = f"{func.__name__}:{args}:{kwargs}"
                result = cache.get(cache_key)
                if result is not None:
                    return result
                result = func(*args, **kwargs)
                cache.set(cache_key, result, timeout)
                return result
            return func(*args, **kwargs)
        return wrapper
    return decorator

def atomic_operation(func):
    """
    Декоратор для атомарных операций с базой данных
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        with transaction.atomic():
            return func(*args, **kwargs)
    return wrapper

def log_execution_time(func):
    """
    Декоратор для логирования времени выполнения функции
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(
            f"{func.__name__} выполнена за {end_time - start_time:.2f} секунд"
        )
        return result
    return wrapper

def require_fields(*required_fields):
    """
    Декоратор для проверки наличия обязательных полей в запросе
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            missing_fields = [
                field for field in required_fields 
                if field not in request.data
            ]
            if missing_fields:
                return {
                    'error': f'Отсутствуют обязательные поля: {", ".join(missing_fields)}'
                }, 400
            return func(request, *args, **kwargs)
        return wrapper
    return decorator