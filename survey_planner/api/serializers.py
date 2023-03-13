from rest_framework import serializers

from drilling_schedule import models


class DrillingScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DrillingSchedule
        fields = ['id', 'imported_schedule', 'version', 'is_converted']
        read_only_fields = ['id', 'is_converted']


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Operation
        fields = [
            'id', 'name', 'start_date', 'end_date', 'meters_drilled', 'well',
            'drilling_schedule',
        ]
