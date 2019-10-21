# Generated by Django 2.2.5 on 2019-10-21 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0006_merge_20191021_1336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscribed_orders',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='subscribed_orders',
            name='start_date',
        ),
        migrations.AddField(
            model_name='subscribed_orders',
            name='delivery_dates',
            field=models.CharField(default=12, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscribed_orders',
            name='delivery_month',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]