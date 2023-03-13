from rest_framework import mixins, viewsets


class RetrieveListModelViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin,
):
    pass


class CreateRetrieveListModelViewSet(
    mixins.CreateModelMixin, RetrieveListModelViewSet,
):
    pass
