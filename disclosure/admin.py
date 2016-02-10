from django.contrib import admin
from django.db import router

for model in admin.site._registry.keys():
    # Eliminate *_raw from the admin panel.
    if router.db_for_write(model=model) != 'default':
        admin.site.unregister(model)
