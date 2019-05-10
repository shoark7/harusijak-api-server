from django.db import models


class Subject(models.Model):
    subject = models.TextField('주제', max_length=20, unique=True)
    guide_format = models.TextField('가이드 형식', blank=True, null=True)
    guide_type = models.CharField(
        '가이드 타입',
        max_length=10,
        choices=(
            ('free', 'free'),
            ('reply', 'reply'),
            ('blank', 'blank'),
            ('constraint', 'constraint'),
        ),
        default='free',
    )

    def __str__(self):
        return self.subject
