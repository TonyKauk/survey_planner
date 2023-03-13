import os

from django.test import TestCase
from django.conf import settings

from ..models import DrillingSchedule


class DrillingScheduleFixture(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        schedule_version = '55.0'
        schedule_file_path = os.path.join(
            settings.BASE_DIR,
            'media/for_testing/Drill_55_0_CSV.csv',
        )
        cls.good_schedule_object = DrillingSchedule.objects.create(
            imported_schedule=schedule_file_path, version=schedule_version,
        )

        cls.good_schedule_object.convert_to_instances()


class BadDrillingScheduleFixture(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bad_schedule_version = '66.0'
        bad_schedule_file_path = os.path.join(
            settings.BASE_DIR,
            'media/for_testing/Drill_55_0_NOT_CSV.txt',
        )
        cls.bad_schedule_object = DrillingSchedule.objects.create(
            imported_schedule=bad_schedule_file_path,
            version=bad_schedule_version,
        )
