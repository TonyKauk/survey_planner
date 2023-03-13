from django.core.validators import FileExtensionValidator
from django.db import models

from .csv_converter import CSVToInstance


class DrillingSchedule(models.Model, CSVToInstance):
    imported_schedule = models.FileField(
        upload_to='drilling_schedules/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['csv'],
                message='Only *.csv files allowed',
            ),
        ],
    )
    version = models.CharField(max_length=20, unique=True)
    is_converted = models.BooleanField(default=False)


class Rig(models.Model):
    name = models.CharField(max_length=20)

    drilling_schedule = models.ForeignKey(
        DrillingSchedule, on_delete=models.CASCADE, related_name='rigs',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['name', 'drilling_schedule'], name='unique_rig'
        )]


class Pad(models.Model):
    name = models.CharField(max_length=20)

    drilling_schedule = models.ForeignKey(
        DrillingSchedule, on_delete=models.CASCADE, related_name='pads',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['name', 'drilling_schedule'], name='unique_pad'
        )]


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

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['name', 'drilling_schedule'], name='unique_well'
        )]


class Operation(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    meters_drilled = models.FloatField()
    duration = models.IntegerField()

    well = models.ForeignKey(
        Well, on_delete=models.CASCADE, related_name='operations',
    )
    drilling_schedule = models.ForeignKey(
        DrillingSchedule, on_delete=models.CASCADE, related_name='operations',
    )

    def save(self, *args, **kwargs):
        self.duration = (self.end_date - self.start_date).days
        super(Operation, self).save(*args, **kwargs)
