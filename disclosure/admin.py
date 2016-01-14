from django.contrib import admin
from django.db import router

for model in admin.site._registry.keys():
    if router.db_for_write(model=model) != 'default':
        admin.site.unregister(model)
