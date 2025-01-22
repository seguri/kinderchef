from datetime import date, datetime
from uuid import uuid4

from django.conf import settings
from django.contrib.admin import display
from django.db import models
from django.utils.translation import gettext_lazy as _
from dateutil.rrule import rrulestr
from zoneinfo import ZoneInfo


def to_datetime(d: date) -> datetime:
    tz = ZoneInfo(settings.TIME_ZONE)
    return datetime(d.year, d.month, d.day, 12, 0, 0, tzinfo=tz)


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

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        get_latest_by = "created_at"

    def __str__(self):
        return f"{self.__class__.__name__} {self.id}"


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


class Child(BaseModel):
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)

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

    def next_occurrence(self):
        try:
            r = rrulestr(self.rrule, cache=True)
            next_occurrence = r.after(to_datetime(date.today()))
            return next_occurrence.date()
        except ValueError:
            return None
