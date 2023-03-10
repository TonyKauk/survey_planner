from drilling_schedule.tests.fixtures import DrillingScheduleFixture
from ..models import Well


class DrillingScheduleModelTest(DrillingScheduleFixture):
    def test_objects_created(self) -> None:
        created_well = Well.objects.filter(name='7472')
        self.assertIsNotNone(created_well)

    def test_well_unique(self) -> None:
        created_well_count = Well.objects.filter(name='7472').count()
        self.assertEqual(created_well_count, 1)

    def test_converted(self) -> None:
        self.assertIs(self.good_schedule_object.is_converted, True)
