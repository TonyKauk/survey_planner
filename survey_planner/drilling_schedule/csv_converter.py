import csv
from datetime import datetime

from models import Operation, Pad, Rig, Well


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
        RIG_PAD_HEADER: ('FRAC', 'Mile', 'WFIS', 'WS')
    }

    def __open_csv__(self):
        with open(self.imported_schedule.path, 'r') as file:
            return csv.reader(file)

    def __get_header_row__(self, csv_reader):
        return next(csv_reader)

    def __make_mapper__(self, csv_reader):
        mapper: dict = {}
        header_row_from_csv = self.__get_header_row__(csv_reader)
        target_headers = [
            header for header in dir(self) if header.endswith('_HEADER')
        ]
        for header in target_headers:
            position_of_header = header_row_from_csv.index(header)
            mapper[header] = position_of_header
        return mapper

    def __filter_row__(self, row, mapper):
        for column in self.EXCESSIVE_ROWS:
            for value in column:
                return row[mapper[column]].startswith(value)

    def __row_to_instances__(self, mapper, csv_reader):
        next(csv_reader)
        for row in csv_reader:
            if (self.__filter_row__(mapper, row) or
                    row[mapper[self.RIG_PAD_HEADER]] == ''):
                pass

            rig_name, pad_name = row[mapper[self.RIG_PAD_HEADER]].split('.')
            rig, created = Rig.objects.get_or_create(
                name=rig_name, drilling_schedule=self,
            )
            if created:
                rig.save()

            pad, created = Pad.objects.get_or_create(
                name=pad_name, drilling_schedule=self,
            )
            if created:
                pad.save()

            well_name = row[mapper[self.WELL_HEADER]]
            well_aim = row[mapper[self.AIM_HEADER]].split('.')[1]
            well, created = Well.objects.get_or_create(
                name=well_name, aim=well_aim, rig=rig, pad=pad,
                drilling_schedule=self,
            )
            if created:
                well.save()

            opertion_name = row[mapper[self.OPERATION_HEADER]]
            operation_start_date_plain = row[mapper[self.START_DATE_HEADER]]
            operation_start_date = datetime.strptime(
                operation_start_date_plain, '%m/%d/%y',
            )
            operation_end_date_plain = row[mapper[self.END_DATE_HEADER]]
            operation_end_date = datetime.strptime(
                operation_end_date_plain, '%m/%d/%y',
            )
            operation_meters_drilled = float(
                row[mapper[self.METERS_DRILLED_HEADER]]
            )
            operation, created = Operation.objects.get_or_create(
                name=opertion_name, start_date=operation_start_date,
                end_date=operation_end_date,
                meters_drilled=operation_meters_drilled, well=well,
                drilling_schedule=self,
            )
            if created:
                operation.save()

    def __switch_to_converted__(self):
        self.converted = True
        self.save()
        pass

    def convert_to_instances(self):
        if self.converted is True:
            pass
        csv_reader = self.__open_csv__()
        mapper = self.__make_mapper__(csv_reader)
        self.__row_to_instances__(mapper=mapper, csv_reader=csv_reader)
        self.__switch_to_converted__()
