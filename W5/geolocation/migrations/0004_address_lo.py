# Generated by Django 3.1.2 on 2020-12-07 14:06

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geolocation', '0003_auto_20201202_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='lo',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326),
        ),
    ]