from django.contrib import admin
from .models import MasterTrader, Signal,CrawlerType,CrawlAssignment,CrawlRunner


class MasterTraderAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_trader_id', 'source', 'is_active')


class SignalAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'external_signal_id', 'symbol', 'type', 'size',
        'price_order', 'stop_loss', 'take_profit',
        'market_price', 'trader', 'time')


# Register your models here.
admin.site.register(MasterTrader, MasterTraderAdmin)
admin.site.register(Signal, SignalAdmin)
admin.site.register(CrawlerType)
admin.site.register(CrawlAssignment)
admin.site.register(CrawlRunner)

