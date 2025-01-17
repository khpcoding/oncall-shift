from django.db import models

class Shift(models.Model):
    day_of_week = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    shift_type = models.CharField(max_length=10, blank=True, null=True)
    date = models.DateField(max_length=10)
    start_time = models.TimeField(max_length=10)
    end_time = models.TimeField(max_length=10)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.date} {self.day_of_week}'