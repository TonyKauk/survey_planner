import csv
from datetime import datetime

from drilling_schedule import models


class CSVToInstance:
    OPERATION_HEADER: str = 'Название работы'
    START_DATE_HEADER: str = 'Начало'
    END_DATE_HEADER: str = 'Окончание'
    METERS_DRILLED_HEADER: str = 'Проходка прогн.,м'
    AIM_HEADER: str = 'Объект/Пласт'
    WELL_HEADER: str = '№ скв. (WBS)'
    RIG_PAD_HEADER: str = 'БУ, Куст'

    EXCESSIVE_ROWS: dict = {
        OPERATION_HEADER: (
            'Complete 208 wells', 'Finish drilling', 'MDT',
            'Start drilling', 'Аварийные работы', 'Ввод скважины',
            'Ввод скважины (БС)', 'Вызов притока (БС)',
            'Вызов притока, очистка ПЗП', 'ГНКТ', 'ГРП',
        ),
        RIG_PAD_HEADER: ('FRAC', 'Mile', 'WFIS', 'WS'),
    }

    def __filter_rows__(self, row: list[str]) -> bool:
        for column in self.EXCESSIVE_ROWS:
            if (row[column].startswith(self.EXCESSIVE_ROWS[column]) or
                    row[self.RIG_PAD_HEADER] == ''):
                return True
        if row[self.AIM_HEADER] == '':
            return True
        if '.' not in row[self.RIG_PAD_HEADER]:
            return True
        return False

    def __format_meters_drilled__(self, meters_drilled: str) -> float:
        if meters_drilled == '':
            meters_drilled = '0.0'
        meters_drilled = float(meters_drilled.replace(',', '.'))
        return meters_drilled

    def __row_to_instances__(self, csv_reader: csv.DictReader) -> None:
        for row in csv_reader:
            if self.__filter_rows__(row):
                continue
            row[self.METERS_DRILLED_HEADER] = self.__format_meters_drilled__(
                row[self.METERS_DRILLED_HEADER]
            )

            rig_name, pad_name = row[self.RIG_PAD_HEADER].split('.')
            rig, created = models.Rig.objects.get_or_create(
                name=rig_name, drilling_schedule=self,
            )
            if created:
                rig.save()

            pad, created = models.Pad.objects.get_or_create(
                name=pad_name, drilling_schedule=self,
            )
            if created:
                pad.save()

            well_name = row[self.WELL_HEADER]
            well_aim = row[self.AIM_HEADER].split('.')[1]
            well, created = models.Well.objects.get_or_create(
                name=well_name, aim=well_aim, rig=rig, pad=pad,
                drilling_schedule=self,
            )
            if created:
                well.save()

            opertion_name = row[self.OPERATION_HEADER]
            operation_start_date_plain = row[self.START_DATE_HEADER]
            operation_start_date = datetime.strptime(
                operation_start_date_plain, '%m/%d/%y',
            )
            operation_end_date_plain = row[self.END_DATE_HEADER]
            operation_end_date = datetime.strptime(
                operation_end_date_plain, '%m/%d/%y',
            )
            operation_meters_drilled = row[self.METERS_DRILLED_HEADER]
            operation, created = models.Operation.objects.get_or_create(
                name=opertion_name, start_date=operation_start_date,
                end_date=operation_end_date,
                meters_drilled=operation_meters_drilled, well=well,
                drilling_schedule=self,
            )
            if created:
                operation.save()

    def __switch_to_converted__(self) -> None:
        self.is_converted = True
        self.save()
        pass

    def convert_to_instances(self) -> None:
        if self.is_converted is True:
            pass
        with open(self.imported_schedule.path, newline='') as csv_file:
            csv_reader = csv.DictReader(
                csv_file, dialect='excel', delimiter=';',
            )
            self.__row_to_instances__(csv_reader=csv_reader)
        self.__switch_to_converted__()
