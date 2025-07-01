from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModeratorCanOnlyChange(BasePermission):
    """
    Модератор может только просматривать и редактировать, но не создавать и не удалять.
    """

    def has_permission(self, request, view):
        user = request.user
        if user.groups.filter(name="Модераторы").exists():
            if request.method in ["POST", "DELETE"]:
                return False
            return True
        return True


class IsOwnerOrReadOnly(BasePermission):
    """
    Обычные пользователи могут редактировать и удалять только свои объекты.
    """

    def has_object_permission(self, request, view, obj):
        # Если модератор - разрешаем всегда
        if request.user.groups.filter(name="Модераторы").exists():
            return True

        # Только владелец может редактировать или удалять
        return obj.owner == request.user
