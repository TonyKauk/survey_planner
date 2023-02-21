from . import models

import os
from django.conf import settings


def test(request):
    schedule_version = '55.0'
    schedule_file_path = os.path.join(
        settings.BASE_DIR,
        'media/for_testing/Drill_55_0_CSV.csv',
    )
    good_schedule_object = models.DrillingSchedule.objects.create(
        imported_schedule=schedule_file_path, version=schedule_version,
    )

    good_schedule_object.convert_to_instances()
    pass
