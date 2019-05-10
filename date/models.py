from datetime import date as dt
from random import randint

from django.db import models

from subject.models import Subject


class Date(models.Model):
    date = models.DateField('날짜')
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING,
                                related_name='used_dates', verbose_name="이 날의 주제")

    @classmethod
    def get_or_create(cls, date=None):
        if date is None:
            date = dt.today()

        if cls.objects.filter(date=date).exists():
            return cls.objects.get(date=date)
        else:
            try:
                max_id = Subject.objects.all().aggregate(max_id=models.Max('id'))['max_id']
            except:
                raise TypeError("Input model should use default integer pk for this function")

            while True:
                pk = randint(1, max_id)
                subject = Subject.objects.filter(pk=pk).first()

                if subject:
                    break

            new_date = cls.objects.create(date=date, subject=subject)
            return new_date

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")
