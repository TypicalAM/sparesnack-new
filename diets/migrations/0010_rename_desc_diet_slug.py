# Generated by Django 4.0.4 on 2022-05-21 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diets', '0009_diet_desc'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diet',
            old_name='desc',
            new_name='slug',
        ),
    ]
