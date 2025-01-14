
from django.core.exceptions import PermissionDenied

def user_has_organization_access(user, organization_id):
    """
    Проверяет, имеет ли пользователь доступ к данной организации.

    Args:
        user: Объект пользователя Django.
        organization_id: ID организации, к которой запрашивается доступ.

    Returns:
        None: Если у пользователя есть доступ.
        Raises PermissionDenied: Если доступа нет.
    """
    if not user.is_authenticated:
        raise PermissionDenied("Пользователь не аутентифицирован.")

    if not hasattr(user, 'organization') or not user.organization:
        raise PermissionDenied("Пользователь не привязан к организации.")

    if user.organization.id != int(organization_id):
        raise PermissionDenied("У пользователя нет доступа к данной организации.")
