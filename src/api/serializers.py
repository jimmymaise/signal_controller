# serializers.py
from rest_framework import serializers

from .models import MasterTrader
from .models import Signal

from .models import CrawlRunner
from .models import CrawlAssignment
from .models import CrawlerType


class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = (
            "id",
            "external_signal_id",
            "symbol",
            "type",
            "size",
            "time",
            "price_order",
            "stop_loss",
            "take_profit",
            "market_price",
        )


class MasterTraderSerializer(serializers.ModelSerializer):
    signals = SignalSerializer(many=True)

    class Meta:
        model = MasterTrader
        fields = ("id", "external_trader_id", "source", "signals")


class SimpleMasterTraderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterTrader
        fields = ("id", "external_trader_id", "source")


class SimpleCrawlRunnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlRunner
        fields = ("name", "crawler_type", "is_active")


class CrawlAssignmentSerializer(serializers.ModelSerializer):
    master_trader = SimpleMasterTraderSerializer()
    crawl_runner = SimpleCrawlRunnerSerializer()

    class Meta:
        model = CrawlAssignment
        fields = ("master_trader", "crawl_runner")


class CrawlRunnerSerializer(serializers.ModelSerializer):
    assignments = CrawlAssignmentSerializer(many=True, required=False)

    class Meta:
        model = CrawlRunner
        fields = ("name", "crawler_type", "is_active", "assignments")


class CrawlerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlerType
        fields = ("name", "source", "is_active")
