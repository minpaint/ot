from rest_framework import permissions


class HasOrganizationPermission(permissions.BasePermission):
    """
    Проверка доступа к объекту на основе организации пользователя.
    """

    def has_permission(self, request, view):
        # Проверяем аутентификацию пользователя
        if not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        # Разрешаем доступ суперпользователю
        if request.user.is_superuser:
            return True

        # Проверяем принадлежность пользователя к организации объекта
        if hasattr(obj, 'organization'):
            return obj.organization in request.user.organizations.all()

        # Если у объекта нет организации, проверяем связанные поля
        if hasattr(obj, 'department'):
            return obj.department.organization in request.user.organizations.all()

        return False