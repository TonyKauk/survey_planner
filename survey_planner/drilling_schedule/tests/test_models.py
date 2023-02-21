from drilling_schedule.tests.fixtures import DrillingScheduleFixture
from ..models import Well


class DrillingScheduleModelTest(DrillingScheduleFixture):
    def test_objects_created(self):
        created_well = Well.objects.filter(name='7472')
        self.assertIsNotNone(created_well)
