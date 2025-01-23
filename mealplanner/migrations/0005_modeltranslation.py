from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mealplanner", "0004_meal"),
    ]

    operations = [
        migrations.AddField(
            model_name="dietaryrestriction",
            name="name_de",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="dietaryrestriction",
            name="name_en",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="dietaryrestriction",
            name="name_it",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="meal",
            name="name_de",
            field=models.CharField(max_length=100, null=True, verbose_name="name"),
        ),
        migrations.AddField(
            model_name="meal",
            name="name_en",
            field=models.CharField(max_length=100, null=True, verbose_name="name"),
        ),
        migrations.AddField(
            model_name="meal",
            name="name_it",
            field=models.CharField(max_length=100, null=True, verbose_name="name"),
        ),
    ]
