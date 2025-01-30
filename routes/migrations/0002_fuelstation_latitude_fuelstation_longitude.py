# Generated by Django 5.1.5 on 2025-01-29 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fuelstation',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fuelstation',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
