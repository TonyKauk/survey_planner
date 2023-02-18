from django.db import models

from csv_converter import CSVToInstance


class DrillingSchedule(models.Model, CSVToInstance):
    imported_schedule = models.FileField(upload_to='drilling_schedules/')
    version = models.CharField(max_length=20)
    converted = models.BooleanField(default=False)


class Rig(models.Model):
    name = models.CharField(max_length=20)

    drilling_schedule = models.ForeignKey(
        DrillingSchedule, on_delete=models.CASCADE, related_name='rigs',
    )


class Pad(models.Model):
    name = models.CharField(max_length=20)

    drilling_schedule = models.ForeignKey(
        DrillingSchedule, on_delete=models.CASCADE, related_name='pads',
    )


class Well(models.Model):
    name = models.CharField(max_length=20)
    aim = models.CharField(max_length=20)

    pad = models.ForeignKey(
        Pad, on_delete=models.CASCADE, related_name='wells',
    )
    rig = models.ForeignKey(
        Rig, on_delete=models.CASCADE, related_name='wells',
    )
    drilling_schedule = models.ForeignKey(
        DrillingSchedule, on_delete=models.CASCADE, related_name='wells',
    )


class Operation(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    meters_drilled = models.FloatField()

    well = models.ForeignKey(
        Well, on_delete=models.CASCADE, related_name='operations',
    )
    drilling_schedule = models.ForeignKey(
        DrillingSchedule, on_delete=models.CASCADE, related_name='operations',
    )
