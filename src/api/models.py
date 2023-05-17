from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Q

SOURCE_CHOICES = (
    ('zulu', 'Zulu Trade'),
)


class MasterTrader(models.Model):
    name = models.CharField(max_length=255, default='default_name')
    external_trader_id = models.CharField(max_length=60)
    source = models.CharField(max_length=255, choices=SOURCE_CHOICES)
    is_active = models.BooleanField(default=True)
    signals = models.JSONField()

    def __str__(self):
        return self.external_trader_id

    class Meta:
        unique_together = ("external_trader_id", "source")


class CrawlerType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    source = models.CharField(max_length=255, choices=SOURCE_CHOICES)
    is_active = models.BooleanField(default=True)


class CrawlRunner(models.Model):
    name = models.CharField(max_length=255)
    crawler_type = models.ForeignKey(CrawlerType, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class CrawlAssignment(models.Model):
    master_trader = models.ForeignKey(MasterTrader, on_delete=models.CASCADE)
    crawl_runner = models.ForeignKey(CrawlRunner, on_delete=models.CASCADE)


@receiver(post_save, sender=MasterTrader)
@receiver(post_save, sender=CrawlRunner)
@receiver(post_delete, sender=MasterTrader)
@receiver(post_delete, sender=CrawlRunner)
def balance_runner_assignment_on_change(sender, **kwargs):
    balance_runner_assignment()


def assign_more_master_traders_to_a_crawl_runner(
        crawl_runner, num_additional_master_trader
):
    unassigned_master_traders = MasterTrader.objects.filter(
        is_active=True, crawl_assignment__isnull=True, source=crawl_runner.source
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
    ).update(crawl_runner=None)

    # Get all active crawl_runners
    active_crawl_runners = CrawlRunner.objects.filter(is_active=True).prefetch_related(
        "assignments"
    )

    # Get the total number of active crawl_runners and active master_traders
    total_active_crawl_runners = active_crawl_runners.values_list('id', flat=True).count()
    total_active_master_traders = MasterTrader.objects.filter(is_active=True).count()

    # Calculate the target number of master_traders per active crawl_runner
    avg_master_traders_per_crawl_runner = (
            total_active_master_traders // total_active_crawl_runners
    )

    # Calculate the number of remaining master_traders that need to be assigned to crawl_runners
    remaining_master_traders = total_active_master_traders % total_active_crawl_runners

    # Get the crawl_runners and the number of master_traders they are currently supporting
    crawl_runners = active_crawl_runners.annotate(
        num_crawled_master_trader=Count("assignments")
    )

    # Sort the crawl_runners by the number of master_traders they are supporting
    crawl_runners = sorted(crawl_runners, key=lambda s: s.num_crawled_master_trader)

    # Reassign master_traders to balance the workload among all crawl_runners
    for crawl_runner in crawl_runners:
        # Calculate the number of additional master_traders that need to be assigned to this crawl_runner
        additional_master_traders = (
                avg_master_traders_per_crawl_runner - crawl_runner.num_crawled_master_trader
        )
        if remaining_master_traders > 0:
            additional_master_traders += 1
            remaining_master_traders -= 1

        if additional_master_traders < 0:
            master_traders_to_unassign = crawl_runner.crawl_assignment.all()[
                                         : abs(additional_master_traders)
                                         ]
            for assignment in master_traders_to_unassign:
                assignment.delete()

        # Assign additional master_traders to this crawl_runner
        if additional_master_traders > 0:
            assign_more_master_traders_to_a_crawl_runner(
                crawl_runner=crawl_runner,
                num_additional_master_trader=additional_master_traders,
            )
