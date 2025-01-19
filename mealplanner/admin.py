from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from mealplanner.models import Child


admin.site.site_header = "KinderChef"
admin.site.site_title = "KinderChef"
admin.site.index_title = _("Meal Planner")


class BaseAdmin(admin.ModelAdmin):
    exclude = ("created_by", "updated_by")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()


@admin.register(Child)
class ChildAdmin(BaseAdmin):
    list_display = ("full_name",)
    list_display_links = ("full_name",)
    search_fields = ("first_name", "last_name")
    ordering = ("first_name",)
