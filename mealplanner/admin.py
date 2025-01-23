from django.contrib import admin
from django.forms import ModelForm
from django.forms.widgets import MultipleHiddenInput
from django.utils.html import format_html_join
from django.utils.translation import gettext_lazy as _

from mealplanner.models import Child, Attendance, DietaryRestriction, Meal

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
    search_fields = ("name",)
    filter_horizontal = ("included_restrictions",)
    form = DietaryRestrictionForm

    def save_model(self, request, obj, form, change):
        if not obj.is_group:
            obj.included_restrictions.clear()
        super().save_model(request, obj, form, change)


@admin.register(Child)
class ChildAdmin(BaseAdmin):
    list_display = ("full_name", "restrictions")
    list_display_links = ("full_name",)
    search_fields = ("first_name", "last_name")
    filter_horizontal = ("dietary_restrictions",)
    ordering = ("first_name",)

    def restrictions(self, obj):
        return len(obj.get_all_dietary_restrictions())


@admin.register(Attendance)
class AttendanceAdmin(BaseAdmin):
    list_display = ("child", "next_occurrence")
    list_display_links = ("child",)


@admin.register(Meal)
class MealAdmin(BaseAdmin):
    list_display = ("name", "link")
    list_display_links = ("name",)
    search_fields = ("name",)
    filter_horizontal = ("dietary_restrictions",)
    readonly_fields = ["restricted_children_display"]

    @admin.display(description=_("Children with Restrictions"))
    def restricted_children_display(self, obj):
        if not obj.pk:
            return "-"

        restricted_children = obj.get_restricted_children()
        if not restricted_children:
            return _("No children are restricted from this meal")

        def args_generator():
            for child in restricted_children:
                yield child.admin_change_url(), child.full_name()

        return format_html_join("\n", "<li><a href='{}'>{}</a></li>", args_generator())
