# serializers.py
from rest_framework import serializers

from .models import MasterTrader


class MasterTraderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MasterTrader
        fields = ('external_trader_id', 'source', 'signals')
