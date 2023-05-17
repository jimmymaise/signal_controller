from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Q
from django.db import transaction

SOURCE_CHOICES = (("zulu", "Zulu Trade"),)


class MasterTrader(models.Model):
    name = models.CharField(max_length=255, default="default_name")
    external_trader_id = models.CharField(max_length=60)
    source = models.CharField(max_length=255, choices=SOURCE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source}|{self.external_trader_id}"

    def update_master_trader_signals(self, updated_signal_list):
        signal_list_from_db = Signal.objects.filter(trader__pk=self.id).values(
            "id", "external_signal_id"
        )
        signal_dict_from_db = {
            signal["external_signal_id"]: signal for signal in signal_list_from_db
        }

        # Prepare data for bulk create/update/delete
        to_create = []
        to_update = []
        for updated_signal in updated_signal_list:
            updated_signal["trader_id"] = self.id
            external_signal_id = str(updated_signal.get("external_signal_id"))

            if exist_signal := signal_dict_from_db.get(external_signal_id):
                to_update.append(Signal(id=exist_signal["id"], **updated_signal))
                del signal_dict_from_db[external_signal_id]
            else:
                to_create.append(Signal(**updated_signal))

        to_delete_ids = [
            signal["id"] for external_signal_id, signal in signal_dict_from_db.items()
        ]

        # Perform database updates within a transaction for consistency
        with transaction.atomic():
            Signal.objects.filter(id__in=to_delete_ids).delete()

            if to_update:
                Signal.objects.bulk_update(
                    to_update,
                    [
                        "symbol",
                        "type",
                        "size",
                        "time",
                        "price_order",
                        "stop_loss",
                        "take_profit",
                        "market_price",
                    ],
                )

            if to_create:
                print(
                    "Signal will be created",
                    [(item.trader_id, item.external_signal_id) for item in to_create],
                )
                Signal.objects.bulk_create(to_create)

    class Meta:
        unique_together = ("external_trader_id", "source")


class Signal(models.Model):
    trader = models.ForeignKey(
        MasterTrader, on_delete=models.CASCADE, related_name="signals"
    )
    external_signal_id = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    size = models.FloatField()
    time = models.DateTimeField()
    price_order = models.FloatField()
    stop_loss = models.FloatField()
    take_profit = models.FloatField()
    market_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.external_signal_id} (from {self.trader.external_trader_id}-{self.trader.source}|updated at {self.time})"

    class Meta:
        unique_together = ("trader", "external_signal_id")


class CrawlerType(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    source = models.CharField(max_length=255, choices=SOURCE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class CrawlRunner(models.Model):
    name = models.CharField(max_length=255, unique=True)
    crawler_type = models.ForeignKey(CrawlerType, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (type: {self.crawler_type})"


class CrawlAssignment(models.Model):
    master_trader = models.ForeignKey(MasterTrader, on_delete=models.CASCADE)
    crawl_runner = models.ForeignKey(
        CrawlRunner, on_delete=models.CASCADE, related_name="assignments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Runner:{self.crawl_runner}|Trader:{self.crawl_runner}"


@receiver(post_save, sender=MasterTrader)
@receiver(post_save, sender=CrawlRunner)
@receiver(post_delete, sender=MasterTrader)
@receiver(post_delete, sender=CrawlRunner)
def balance_runner_assignment_on_change(sender, **kwargs):
    if "created" not in kwargs or kwargs["created"] == True or kwargs["update_fields"]:
        balance_runner_assignment()


def assign_more_master_traders_to_a_crawl_runner(
    crawl_runner, num_additional_master_trader
):
    unassigned_master_traders = MasterTrader.objects.filter(
        is_active=True,
        crawlassignment__isnull=True,
        source=crawl_runner.crawler_type.source,
    )

    CrawlAssignment.objects.bulk_create(
        [
            CrawlAssignment(master_trader=master_trader, crawl_runner=crawl_runner)
            for master_trader in unassigned_master_traders[
                :num_additional_master_trader
            ]
        ]
    )


def balance_runner_assignment():
    # Un-assign inactive master_traders and inactive crawl_runners
    CrawlAssignment.objects.filter(
        Q(master_trader__is_active=False)
        | Q(master_trader__isnull=True)
        | Q(crawl_runner__is_active=False)
        | Q(crawl_runner__isnull=True)
    ).delete()

    # Get all active crawl_runners
    active_crawl_runners = (
        CrawlRunner.objects.filter(is_active=True)
        .annotate(num_assignments=Count("assignments"))
        .prefetch_related("assignments")
        .order_by("-num_assignments")
    )

    # Get the total number of active crawl_runners and active master_traders
    total_active_crawl_runners = active_crawl_runners.values_list(
        "id", flat=True
    ).count()
    total_active_master_traders = MasterTrader.objects.filter(is_active=True).count()

    if not all([total_active_master_traders, total_active_crawl_runners]):
        return

    # Calculate the target number of master_traders per active crawl_runner
    avg_master_traders_per_crawl_runner = (
        total_active_master_traders // total_active_crawl_runners
    )

    # Calculate the number of remaining master_traders that need to be assigned to crawl_runners
    remaining_master_traders = total_active_master_traders % total_active_crawl_runners

    # Reassign master_traders to balance the workload among all crawl_runners
    for crawl_runner in active_crawl_runners:
        # Calculate the number of additional master_traders that need to be assigned to this crawl_runner
        additional_master_traders = (
            avg_master_traders_per_crawl_runner - crawl_runner.num_assignments
        )
        if remaining_master_traders > 0:
            additional_master_traders += 1
            remaining_master_traders -= 1

        if additional_master_traders < 0:
            assignment_to_delete = crawl_runner.assignments.all()[
                : abs(additional_master_traders)
            ]
            assignment_ids_to_delete = [
                assignment.id for assignment in assignment_to_delete
            ]
            CrawlAssignment.objects.filter(id__in=assignment_ids_to_delete).delete()

        # Assign additional master_traders to this crawl_runner
        if additional_master_traders > 0:
            assign_more_master_traders_to_a_crawl_runner(
                crawl_runner=crawl_runner,
                num_additional_master_trader=additional_master_traders,
            )
