# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='spot',
            name='lat',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='spot',
            name='lng',
            field=models.FloatField(null=True),
        ),
    ]
