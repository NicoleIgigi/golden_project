# Generated by Django 5.1.1 on 2024-09-21 11:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='building',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='maintenancerequest',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='resident',
            options={'ordering': ['last_name', 'first_name']},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['building', 'room_number']},
        ),
        migrations.AlterField(
            model_name='building',
            name='total_rooms',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='room',
            name='capacity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
