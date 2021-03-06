# Generated by Django 2.0.5 on 2018-09-20 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carpooling', '0015_auto_20180920_1112'),
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_defaulttrip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carpooling.DefaultTrip')),
                ('user_proposition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carpooling.Proposition')),
            ],
        ),
        migrations.AddField(
            model_name='proposition',
            name='passenger',
            field=models.ManyToManyField(null=True, related_name='passenger', through='carpooling.Register', to='carpooling.DefaultTrip'),
        ),
    ]
