from django.contrib import admin

from .ballot import urlpatterns as b_urls
from .office_election import urlpatterns as oe_urls
from .referendum import urlpatterns as r_urls


admin.autodiscover()

urlpatterns = b_urls + oe_urls + r_urls
