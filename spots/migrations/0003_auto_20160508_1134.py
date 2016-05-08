# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spots', '0002_auto_20160508_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spot',
            name='lat',
            field=models.DecimalField(decimal_places=8, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='spot',
            name='lng',
            field=models.DecimalField(decimal_places=8, max_digits=11, null=True),
        ),
        migrations.AlterField(
            model_name='spot',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
