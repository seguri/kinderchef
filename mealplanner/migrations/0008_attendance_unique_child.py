from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mealplanner", "0007_weeklyschedule"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="attendance",
            constraint=models.UniqueConstraint(fields=("child",), name="unique_child"),
        ),
    ]
