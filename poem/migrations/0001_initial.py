# Generated by Django 2.1.5 on 2019-01-19 06:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Poem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('written_date', models.DateField(auto_now_add=True, verbose_name='작성 날짜')),
                ('written_time', models.TimeField(auto_now_add=True, verbose_name='작성 시간')),
                ('subject', models.CharField(blank=True, default='자유주제', max_length=20, verbose_name='주제')),
                ('title', models.CharField(max_length=30, verbose_name='제목')),
                ('content', models.TextField()),
                ('background', models.ImageField(blank=True, null=True, upload_to='background/', verbose_name='배경지')),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('displayed', models.BooleanField(default=True)),
                ('writer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poems', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
