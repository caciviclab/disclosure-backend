from rest_framework.views import get_view_name

from swagger_nickname_registry import resolve_nicknames


def view_name(cls, suffix=None):
    """Transform the view to a nickname. In the following order
    1. Return a registered nickname
    2. Rename "retrieve" to "get"
    3. Return just the suffix
    4. Return the default nickname.
    """
    def name_to_nick(cls, suffix=None):
        if not suffix:
            return get_view_name(cls, suffix).lower()
        elif suffix.lower() == 'retrieve':
            return 'get'
        else:
            return suffix.lower()

    return resolve_nicknames(cls, suffix=suffix, default_func=name_to_nick)
