"""
Provides the swagger "nickname" field, a friendly name for the swagger client methods.
"""


def view_name(cls, suffix=None):
    if suffix:
        return suffix.lower()

    # Fallback to django-rest-swagger's default
    return None
