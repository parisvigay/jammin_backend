# Generated by Django 4.2.7 on 2023-11-22 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_band_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rehearsal',
            name='notes',
            field=models.TextField(max_length=2000),
        ),
    ]
