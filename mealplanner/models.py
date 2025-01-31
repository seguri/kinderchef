from datetime import date, datetime
from uuid import uuid4
from zoneinfo import ZoneInfo

from dateutil.rrule import rrulestr
from django.conf import settings
from django.contrib.admin import display
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def to_aware_datetime(d: date) -> datetime:
    return to_naive_datetime(d).replace(tzinfo=ZoneInfo(settings.TIME_ZONE))


def to_naive_datetime(d: date) -> datetime:
    return datetime(d.year, d.month, d.day, 12, 0, 0)


def validate_monday(value):
    if value.isocalendar().weekday != 1:
        raise ValidationError(_("%(value)s must be a Monday"), params={"value": value})


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Managed in admin.py
    # If you create objects outside the admin interface, you won't be able to provide these required values.
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_created_by",
        on_delete=models.PROTECT,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_updated_by",
        on_delete=models.PROTECT,
    )

    def admin_change_url(self):
        viewname = f"admin:{self._meta.app_label}_{self._meta.model_name}_change"
        return reverse(viewname, args=(self.pk,))

    def __str__(self):
        return f"{self.__class__.__name__} {self.id}"

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        get_latest_by = "created_at"


class DietaryRestriction(BaseModel):
    name = models.CharField(max_length=100)
    is_group = models.BooleanField(default=False)
    included_restrictions = models.ManyToManyField(
        "self", blank=True, symmetrical=False
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = _("Dietary restriction")
        verbose_name_plural = _("Dietary restrictions")


class Child(BaseModel):
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)
    dietary_restrictions = models.ManyToManyField(
        DietaryRestriction, blank=True, related_name="children"
    )

    def get_all_dietary_restrictions(self):
        restrictions = self.dietary_restrictions.all()
        return DietaryRestriction.objects.filter(
            Q(id__in=restrictions) | Q(included_restrictions__id__in=restrictions)
        ).distinct()

    @display(description=_("full name"))
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()

    class Meta:
        ordering = ["first_name", "last_name"]
        unique_together = ["first_name", "last_name"]
        verbose_name = _("Child")
        verbose_name_plural = _("Children")


class Attendance(BaseModel):
    child = models.ForeignKey("Child", on_delete=models.CASCADE)
    rrule = models.TextField()

    @display(boolean=True, description=_("Is today coming?"))
    def is_today_coming(self):
        today = date.today()
        # Any minute after midnight marks today as "lost", even with inc=True
        today_midnight = datetime(today.year, today.month, today.day, 0, 0, 0)
        try:
            r = rrulestr(self.rrule, cache=True)
            next_occurrence = r.after(today_midnight, inc=True)
            return next_occurrence.date() == today
        except ValueError:
            return False

    @display(description=_("Next occurrence"))
    def next_occurrence(self):
        try:
            r = rrulestr(self.rrule, cache=True)
            next_occurrence = r.after(to_naive_datetime(date.today()))
            return next_occurrence.date()
        except ValueError:
            return None

    def __str__(self):
        return f"{self.child}, {self.next_occurrence()}"

    class Meta:
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")
        constraints = (models.UniqueConstraint(fields=["child"], name="unique_child"),)


class Meal(BaseModel):
    name = models.CharField(_("name"), max_length=100)
    link = models.URLField(_("link"), blank=True)
    notes = models.TextField(_("notes"), blank=True)
    dietary_restrictions = models.ManyToManyField(
        DietaryRestriction, blank=True, related_name="meals"
    )

    def get_restricted_children(self):
        meal_restrictions = self.dietary_restrictions.all()
        return (
            Child.objects.filter(
                Q(dietary_restrictions__in=meal_restrictions)
                | Q(dietary_restrictions__included_restrictions__in=meal_restrictions)
            )
            .distinct()
            .order_by("first_name", "last_name")
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Meal")
        verbose_name_plural = _("Meals")


class WeeklySchedule(BaseModel):
    week_start = models.DateField(_("Start of the week"), validators=[validate_monday])
    notes = models.TextField(_("notes"), blank=True)
    monday_meal = models.ForeignKey(
        Meal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="monday_meal",
        verbose_name=_("Monday meal"),
    )
    tuesday_meal = models.ForeignKey(
        Meal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tuesday_meal",
        verbose_name=_("Tuesday meal"),
    )
    wednesday_meal = models.ForeignKey(
        Meal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="wednesday_meal",
        verbose_name=_("Wednesday meal"),
    )
    thursday_meal = models.ForeignKey(
        Meal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="thursday_meal",
        verbose_name=_("Thursday meal"),
    )
    friday_meal = models.ForeignKey(
        Meal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="friday_meal",
        verbose_name=_("Friday meal"),
    )

    @property
    def week(self):
        return self.week_start.isocalendar().week

    @property
    def year(self):
        return self.week_start.isocalendar().year

    def __str__(self):
        return f"Week {self.week} of {self.year}, starting on {self.week_start}"

    class Meta:
        ordering = ["-week_start"]
        verbose_name = _("Weekly schedule")
        verbose_name_plural = _("Weekly schedules")
        constraints = (
            models.UniqueConstraint(fields=["week_start"], name="unique_week_start"),
        )
