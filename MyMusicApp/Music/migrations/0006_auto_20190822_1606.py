# Generated by Django 2.2.2 on 2019-08-22 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Music', '0005_remove_artist_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='artist_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]