# Create your views here.
# views.py
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from . import models, serializers
from .models import MasterTrader, Signal
from .serializers import MasterTraderSerializer, SignalSerializer


class MultipleFieldLookupORMixin(object):
    """
    Actual code http://www.django-rest-framework.org/api-guide/generic-views/#creating-custom-mixins
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            try:  # Get the result with one or more fields.
                filter[field] = self.kwargs[field]
            except Exception:
                pass
        return get_object_or_404(queryset, **filter)  # Lookup the object


class MasterTraderViewSet(viewsets.ModelViewSet):
    queryset = MasterTrader.objects.all().order_by('id')
    serializer_class = MasterTraderSerializer

    def create(self, request, *args, **kwargs):
        # Create a new dictionary with only the fields defined in the serializer
        filtered_data = {k: v for k, v in request.data.items() if k in MasterTraderSerializer.Meta.fields}

        # Use the filtered data to update or create the MasterTrader instance
        signals = filtered_data.pop('signals')
        master_trader, created = MasterTrader.objects.update_or_create(
            external_trader_id=request.data.get('external_trader_id'),
            source=request.data.get('source'),
            defaults=filtered_data
        )

        # Serialize the MasterTrader instance and return it in the response
        master_trader.update_master_trader_signals(signals)
        serializer = MasterTraderSerializer(master_trader, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class MasterTraderRetrieveView(MultipleFieldLookupORMixin, generics.RetrieveAPIView):
    queryset = models.MasterTrader.objects.all()
    serializer_class = serializers.MasterTraderSerializer
    lookup_fields = ['source', 'external_trader_id']


class SignalViewSet(viewsets.ModelViewSet):
    queryset = Signal.objects.all()
    serializer_class = SignalSerializer
