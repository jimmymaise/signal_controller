from django.contrib import admin
from .models import MasterTrader, Signal, CrawlerType, CrawlAssignment, CrawlRunner


def _save_model(request, obj, form, change):
    update_fields = set()
    if change:
        for key, value in form.cleaned_data.items():
            # assuming that you have ManyToMany fields that are called groups and user_permissions
            # we want to avoid adding them to update_fields
            if key in ["user_permissions", "groups"]:
                continue
            if value != form.initial[key]:
                update_fields.add(key)

    obj.save(update_fields=update_fields)


class MasterTraderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "external_trader_id",
        "source",
        "is_active",
        "updated_at",
        "created_at",
    )

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if change:
            _save_model(request, obj, form, change)
        else:
            super().save_model(request, obj, form, change)


class SignalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "external_signal_id",
        "symbol",
        "type",
        "size",
        "price_order",
        "stop_loss",
        "take_profit",
        "market_price",
        "trader",
        "time",
        "updated_at",
        "created_at",
    )


class CrawlRunnerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "crawler_type",
        "is_active",
        "updated_at",
        "created_at",
    )

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if change:
            _save_model(request, obj, form, change)
        else:
            super().save_model(request, obj, form, change)


class CrawlerTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "source",
        "is_active",
        "updated_at",
        "created_at",
    )

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        _save_model(request, obj, form, change)


class CrawlAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "master_trader",
        "crawl_runner",
        "updated_at",
        "created_at",
    )

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        _save_model(request, obj, form, change)


# Register your models here.
admin.site.register(MasterTrader, MasterTraderAdmin)
admin.site.register(Signal, SignalAdmin)
admin.site.register(CrawlerType, CrawlerTypeAdmin)
admin.site.register(CrawlAssignment, CrawlAssignmentAdmin)
admin.site.register(CrawlRunner, CrawlRunnerAdmin)
