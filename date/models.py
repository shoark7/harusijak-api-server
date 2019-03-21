from datetime import date
from random import randint

from django.db import models

from subject.models import Subject

TODAY = date.today()


class Date(models.Model):
    date = models.DateField('날짜', unique_for_date=True, default=date.today)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING,
                                related_name='used_dates', verbose_name="이 날의 주제")

    def get_or_create(date=TODAY):
        if self.objects.filter(date=date).exists():
            return self.objects.get(date=date)
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

            new_date = self.objects.create(date, subject=subject)
            return new_date

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")
