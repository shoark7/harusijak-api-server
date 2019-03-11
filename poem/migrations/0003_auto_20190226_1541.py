# Generated by Django 2.1.5 on 2019-02-26 06:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('poem', '0002_auto_20190122_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='poem',
            name='title',
            field=models.CharField(max_length=12, verbose_name='제목'),
        ),
        migrations.AddField(
            model_name='like',
            name='poem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poem.Poem'),
        ),
        migrations.AddField(
            model_name='like',
            name='poet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]