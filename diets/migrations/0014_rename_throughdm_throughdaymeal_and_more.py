# Generated by Django 4.0.4 on 2022-05-27 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("diets", "0013_rename_intermediarydaymeal_throughdm_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ThroughDM",
            new_name="ThroughDayMeal",
        ),
        migrations.RenameModel(
            old_name="ThroughMI",
            new_name="ThroughMealIngr",
        ),
    ]