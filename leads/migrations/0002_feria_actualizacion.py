# Generated by Django 5.2.1 on 2025-07-11 16:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Actualizacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idioma', models.CharField(choices=[('es', 'Español'), ('en', 'Inglés')], max_length=10)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('feria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.feria')),
            ],
            options={
                'unique_together': {('feria', 'idioma')},
            },
        ),
    ]
