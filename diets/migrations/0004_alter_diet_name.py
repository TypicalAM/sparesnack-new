# Generated by Django 4.0.6 on 2022-07-23 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("diets", "0003_alter_diet_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="diet",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
