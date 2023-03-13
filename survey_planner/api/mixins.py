from rest_framework import mixins, viewsets


class CreateRetrieveListModelViewSet(
    mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet,
):
    pass
