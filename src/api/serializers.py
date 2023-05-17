# serializers.py
from rest_framework import serializers

from .models import MasterTrader
from .models import Signal


class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = (
            'id', 'external_signal_id', 'symbol', 'type', 'size', 'time', 'price_order', 'stop_loss', 'take_profit',
            'market_price')


class MasterTraderSerializer(serializers.ModelSerializer):
    signals = SignalSerializer(many=True)

    class Meta:
        model = MasterTrader
        fields = ('id', 'external_trader_id', 'source', 'signals')
