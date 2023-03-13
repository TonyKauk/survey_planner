from django.core.exceptions import ValidationError

from drilling_schedule.tests.fixtures import (
    DrillingScheduleFixture, BadDrillingScheduleFixture,
)
from ..models import Well, Operation


class DrillingScheduleModelTest(
    DrillingScheduleFixture, BadDrillingScheduleFixture,
):
    def test_objects_created(self) -> None:
        TESTED_WELL_NAME = '7472'

        created_well = Well.objects.filter(name=TESTED_WELL_NAME)
        self.assertIsNotNone(created_well)

    def test_well_unique(self) -> None:
        TESTED_WELL_NAME = '7472'

        created_well_count = Well.objects.filter(
            name=TESTED_WELL_NAME
        ).count()
        self.assertEqual(created_well_count, 1)

    def test_converted(self) -> None:
        self.assertIs(self.good_schedule_object.is_converted, True)

    def test_file_type_validation(self) -> None:
        self.assertRaises(
            ValidationError, self.bad_schedule_object.full_clean
        )

    def test_operation_exists(self) -> None:
        TESTED_WELL_NAME = '2072'
        TESTED_OPERATION_NAME = 'Кондуктор 324мм'

        well = Well.objects.get(name=TESTED_WELL_NAME)
        created_operation = Operation.objects.get(
            name=TESTED_OPERATION_NAME, well=well,
        )
        self.assertIsNotNone(created_operation)

    def test_duration(self) -> None:
        TESTED_WELL_NAME = '8071'
        TESTED_OPERATION_NAME = 'Направление 426мм'
        TESTED_DURATION = 3

        tested_operation = Operation.objects.get(
            well__name=TESTED_WELL_NAME, name=TESTED_OPERATION_NAME,
        )
        self.assertEqual(tested_operation.duration, TESTED_DURATION)
