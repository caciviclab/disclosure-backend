class DisclosureRouter(object):
    """
    Allow calaccess_raw and netfile_raw to talk
    to their own databases, separately from the
    main app.
    """
    def get_db(self, model=None, app_label=None):
        app_label = app_label or model._meta.app_label
        if app_label.endswith('_raw'):
            db_label = 'calaccess_raw'
        else:
            db_label = 'default'
        return db_label

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        return self.get_db(model=model)

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        return self.get_db(model=model)

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        return self.get_db(model=obj1) == self.get_db(model=obj2)

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        intended_db = self.get_db(app_label=app_label)
        return (db == intended_db) or (db == 'default' and intended_db is None)
