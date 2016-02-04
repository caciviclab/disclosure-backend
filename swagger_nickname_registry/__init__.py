from rest_framework.views import get_view_name


API_NICKNAMES = dict()


def swagger_nickname(nickname):
    def decorator(func):
        # Works on view functions
        key = func.func_name
        API_NICKNAMES[key] = nickname

        # Works on view classes
        func.swagger_nickname = nickname

        return func
    return decorator


def resolve_nicknames(cls, suffix=None, default_func=get_view_name):
    # Lowercase the default nickname. Default from:
    # http://www.django-rest-framework.org/api-guide/settings/#view_name_function
    try:
        if hasattr(cls, suffix):  # View classes
            func = getattr(cls, suffix, None)
            nickname = getattr(func, 'swagger_nickname', None)

        else:  # View functions
            nickname = API_NICKNAMES.get(cls.as_view().func_name)
    except:
        nickname = None

    return nickname or default_func(cls, suffix)
