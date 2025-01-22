from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mealplanner", "0002_dietaryrestriction"),
    ]

    operations = [
        migrations.AddField(
            model_name="child",
            name="dietary_restrictions",
            field=models.ManyToManyField(
                blank=True, related_name="children", to="mealplanner.dietaryrestriction"
            ),
        ),
    ]
