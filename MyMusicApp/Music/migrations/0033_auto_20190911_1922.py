# Generated by Django 2.2.2 on 2019-09-11 18:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Music', '0032_auto_20190911_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='music',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]