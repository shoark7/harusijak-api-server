import uuid

from django.db import models

from poet.models import Poet


class Poem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    writer = models.ForeignKey(Poet, related_name='poems', on_delete=models.CASCADE)
    written_date = models.DateField('작성 날짜', auto_now_add=True)
    written_time = models.TimeField('작성 시간', auto_now_add=True)

    subject = models.CharField('주제', max_length=20, blank=True, default='자유주제')
    title = models.CharField('제목', max_length=30)
    content = models.TextField()
    background = models.ImageField('배경지', upload_to='background/', blank=True, null=True)

    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    displayed = models.BooleanField(default=True)

    def __str__(self):
        return  {'title': self.title,
                 'writer': self.writer.id,
                 'subject': self.subject,
                }
