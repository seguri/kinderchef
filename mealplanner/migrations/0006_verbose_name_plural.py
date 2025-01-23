from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mealplanner", "0005_modeltranslation"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="attendance",
            options={
                "verbose_name": "Attendance",
                "verbose_name_plural": "Attendances",
            },
        ),
        migrations.AlterModelOptions(
            name="dietaryrestriction",
            options={
                "ordering": ["name"],
                "verbose_name": "Dietary restriction",
                "verbose_name_plural": "Dietary restrictions",
            },
        ),
        migrations.AlterModelOptions(
            name="meal",
            options={"verbose_name": "Meal", "verbose_name_plural": "Meals"},
        ),
    ]
