# Generated by Django 4.0.4 on 2022-05-27 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("diets", "0011_meal_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="diet",
            name="public",
            field=models.BooleanField(default=True),
        ),
    ]