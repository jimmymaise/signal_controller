from django.db import models


class MasterTrader(models.Model):
    external_trader_id = models.CharField(max_length=60)
    source = models.CharField(max_length=60)
    signals = models.JSONField()

    def __str__(self):
        return self.external_trader_id

    class Meta:
        unique_together = ('external_trader_id', 'source')
