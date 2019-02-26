import uuid

from django.db import models

from poet.models import Poet

from harusijak.storage_backends import PoemMediaStorage


class Poem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    writer = models.ForeignKey(Poet, related_name='poems', on_delete=models.CASCADE)
    written_date = models.DateField('작성 날짜', auto_now_add=True)
    written_time = models.TimeField('작성 시간', auto_now_add=True)

    subject = models.CharField('주제', max_length=20, blank=True, default='자유주제')
    title = models.CharField('제목', max_length=12)
    content = models.TextField()
    background = models.ImageField('배경지', storage=PoemMediaStorage(), blank=True, null=True)
    # align = models.CharField(
        # max_length=9,
        # choices=(
            # ('right', 'right'),
            # ('center', 'center'),
            # ('left', 'left'),
        # ),
        # default='center',
    # )

    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    displayed = models.BooleanField(default=True)

    def __str__(self):
        return self.title + ': ' + self.content[:10]

    class Meta:
        ordering = ['-written_date', '-written_time',]


class Like(models.Model):
    poet = models.ForeignKey(Poet, on_delete=models.CASCADE)
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.poet.nickname} likes \'{self.poem.title[:10]}\''


class Dislike(models.Model):
    poet = models.ForeignKey(Poet, on_delete=models.CASCADE)
    poem = models.ForeignKey(Poem, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.poet.nickname} dislikes \'{self.poem.title[:10]}\''
