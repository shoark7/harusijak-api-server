# Generated by Django 2.1.5 on 2019-03-21 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='guide_format',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='가이드 형식'),
        ),
    ]
