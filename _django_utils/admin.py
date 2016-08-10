from django.contrib import admin


def validate_and_register_admin(model, admin_cls, num_hidden_fields):
    """Validate that model and admin have expected field differences."""
    _fld_set_master = set([fld.name for fld in model._meta.get_fields()])
    _fld_set_admin = set((admin_cls.fields or tuple()) +
                         (admin_cls.readonly_fields or tuple()))

    assert len(_fld_set_master - _fld_set_admin) == num_hidden_fields, \
        "New missing field in %s: one of %s" % (
            admin_cls.__name__, _fld_set_master - _fld_set_admin)
    assert len(_fld_set_admin - _fld_set_master) == 0, \
        "%s: field eliminated: %s" % (
            admin_cls.__name__, _fld_set_admin - _fld_set_master)

    # Validated, now register.
    admin.site.register(model, admin_cls)
