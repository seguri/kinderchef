import django.db.models.deletion
import mealplanner.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mealplanner", "0006_verbose_name_plural"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="WeeklySchedule",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "week_start",
                    models.DateField(
                        validators=[mealplanner.models.validate_monday],
                        verbose_name="Start of the week",
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="notes")),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "friday_meal",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="friday_meal",
                        to="mealplanner.meal",
                        verbose_name="Friday meal",
                    ),
                ),
                (
                    "monday_meal",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="monday_meal",
                        to="mealplanner.meal",
                        verbose_name="Monday meal",
                    ),
                ),
                (
                    "thursday_meal",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="thursday_meal",
                        to="mealplanner.meal",
                        verbose_name="Thursday meal",
                    ),
                ),
                (
                    "tuesday_meal",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="tuesday_meal",
                        to="mealplanner.meal",
                        verbose_name="Tuesday meal",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "wednesday_meal",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="wednesday_meal",
                        to="mealplanner.meal",
                        verbose_name="Wednesday meal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Weekly schedule",
                "verbose_name_plural": "Weekly schedules",
                "ordering": ["-week_start"],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("week_start",), name="unique_week_start"
                    )
                ],
            },
        ),
    ]
