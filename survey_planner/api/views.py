from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import serializers
from . import mixins
from drilling_schedule import models


class DrillingScheduleViewSet(mixins.CreateRetrieveListModelViewSet):
    queryset = models.DrillingSchedule.objects.all()
    serializer_class = serializers.DrillingScheduleSerializer

    @action(methods=['post'], detail=True)
    def convert_to_operations(self, request, pk):
        schedule = get_object_or_404(models.DrillingSchedule, id=pk)
        result: str = schedule.convert_to_instances()
        return Response({'result': result}, status=status.HTTP_200_OK)


class OperationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.OperationSerializer

    def get_queryset(self):
        return models.Operation.objects.filter(
            drilling_schedule__id=self.kwargs['schedule_id']
        )
