# Generated by Django 4.1.7 on 2023-04-12 22:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0004_alter_signal_market_price_alter_signal_stop_loss_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="signal",
            name="time",
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]
