# Generated by Django 4.1.7 on 2023-03-13 20:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0006_remove_signal_limit"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="signal",
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name="crawlertype",
            name="id",
        ),
        migrations.AlterField(
            model_name="crawlertype",
            name="name",
            field=models.CharField(
                max_length=255, primary_key=True, serialize=False, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="crawlrunner",
            name="name",
            field=models.CharField(max_length=255, unique=True),
        ),
    ]