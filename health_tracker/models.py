import datetime

from django.conf import settings
from django.db import models

# Create your models here.
from django.urls import reverse


class Date(models.Model):
    DAY = "DAY"
    WEEK = "WEEK"

    OPTION = [(DAY, 'Day'), (WEEK, 'Week')]

    date=models.DateField(default=datetime.date.today)
    option=models.TextField(choices=OPTION)

    def __str__(self):
        return self.date.__str__()

    def get_absolute_url(self):
        return reverse('health_tracker:date_detail', args=[self.pk])


class Value(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date=models.ForeignKey(Date,on_delete=models.CASCADE)
    value = models.IntegerField()

    def get_absolute_url(self):
        return reverse('health_tracker:value_detail', args=[self.pk])

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    date = models.ForeignKey(Date,on_delete=models.CASCADE)
    rating = models.IntegerField()

    def get_absolute_url(self):
        return reverse('health_tracker:rating_detail', args=[self.pk])
