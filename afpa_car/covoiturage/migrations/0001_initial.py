# Generated by Django 2.0.6 on 2018-07-16 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adress_label', models.CharField(max_length=50, verbose_name="Libellé de l'adresse")),
                ('street', models.TextField(max_length=50, verbose_name='Nom de la rue')),
                ('street_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='Numéro de la rue')),
                ('street_complement', models.CharField(blank=True, max_length=50, null=True, verbose_name="Complément d'adresse")),
                ('lattitude', models.DecimalField(decimal_places=25, max_digits=25, verbose_name='lattitude')),
                ('longitude', models.DecimalField(decimal_places=25, max_digits=25, verbose_name='longitude')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=25, verbose_name='Ville')),
            ],
        ),
        migrations.CreateModel(
            name='ZipCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip_code', models.IntegerField(max_length=5, verbose_name='Code postal')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='zipCode',
            field=models.ManyToManyField(to='covoiturage.ZipCode', verbose_name='Code postal'),
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covoiturage.City', verbose_name='Ville'),
        ),
        migrations.AddField(
            model_name='address',
            name='zipCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covoiturage.ZipCode', verbose_name='Code Postal'),
        ),
    ]
