from django.contrib import admin
from django.forms import ModelForm
from django.forms.widgets import MultipleHiddenInput
from django.utils.translation import gettext_lazy as _

from mealplanner.models import Child, Attendance, DietaryRestriction

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

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        # Delete objects marked for deletion
        for obj in formset.deleted_objects:
            obj.delete()

        # Update existing instances
        for instance in instances:
            if not hasattr(instance, "created_by") or instance.created_by is None:
                instance.created_by = request.user
            instance.updated_by = request.user
            instance.save()

        formset.save_m2m()


class DietaryRestrictionForm(ModelForm):
    class Meta:
        model = DietaryRestriction
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.is_group:
            self.fields["included_restrictions"].queryset = (
                DietaryRestriction.objects.filter(is_group=False)
            )
        else:
            self.fields["included_restrictions"].widget = MultipleHiddenInput()
            self.initial["included_restrictions"] = []


@admin.register(DietaryRestriction)
class DietaryRestrictionAdmin(BaseAdmin):
    list_display = ("name", "is_group")
    filter_horizontal = ("included_restrictions",)
    form = DietaryRestrictionForm

    def save_model(self, request, obj, form, change):
        if not obj.is_group:
            obj.included_restrictions.clear()
        super().save_model(request, obj, form, change)


@admin.register(Child)
class ChildAdmin(BaseAdmin):
    list_display = ("full_name",)
    list_display_links = ("full_name",)
    search_fields = ("first_name", "last_name")
    ordering = ("first_name",)


@admin.register(Attendance)
class AttendanceAdmin(BaseAdmin):
    list_display = ("child", "next_occurrence")
    list_display_links = ("child",)
