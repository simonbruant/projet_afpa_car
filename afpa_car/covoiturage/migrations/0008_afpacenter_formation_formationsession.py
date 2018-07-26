# Generated by Django 2.0.5 on 2018-07-26 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('covoiturage', '0007_car_amount_of_free_seats'),
    ]

    operations = [
        migrations.CreateModel(
            name='AfpaCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('center_name', models.CharField(max_length=50)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covoiturage.Address', verbose_name='Adresse')),
            ],
        ),
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formation_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='FormationSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formation_session_start_date', models.DateField()),
                ('formation_session_end_date', models.DateField()),
                ('work_experience_start_date', models.DateField()),
                ('work_experience_end_date', models.DateField()),
                ('afpa_center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covoiturage.AfpaCenter', verbose_name='Centre Afpa')),
                ('formation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covoiturage.Formation', verbose_name='Formation')),
            ],
        ),
    ]