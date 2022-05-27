# Generated by Django 4.0.4 on 2022-05-27 20:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("diets", "0017_alter_diet_options_alter_meal_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="day",
            name="date",
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name="diet",
            name="date",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
