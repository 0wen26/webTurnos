# Generated by Django 5.0.7 on 2024-09-11 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.CharField(max_length=100)),
                ('nombre_turno', models.CharField(max_length=100)),
                ('nombres', models.JSONField()),
            ],
        ),
    ]
