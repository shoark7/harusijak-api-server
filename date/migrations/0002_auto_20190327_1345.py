# Generated by Django 2.1.5 on 2019-03-27 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('date', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='date',
            field=models.DateField(unique_for_date=True, verbose_name='날짜'),
        ),
    ]
