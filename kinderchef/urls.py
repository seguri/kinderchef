from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path(_("admin/"), admin.site.urls),
)

urlpatterns += debug_toolbar_urls()
