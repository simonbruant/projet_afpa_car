# Generated by Django 2.0.5 on 2018-09-13 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpooling', '0005_defaulttrip_is_driver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaulttrip',
            name='is_driver',
            field=models.BooleanField(default=False, verbose_name='conducteur ou passager'),
        ),
    ]
